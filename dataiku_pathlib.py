import dataiku
from pathlib import PurePosixPath
from fnmatch import fnmatch
from io import BytesIO, StringIO
from PIL import Image
import numpy as np
from typing import Union, Optional, List, IO, Tuple
import numpy.typing as ntp

class Folder(dataiku.Folder):
    def __init__(self, lookup, project_key=None, ignore_flow=False):
        super().__init__(lookup, project_key, ignore_flow)

    def glob(self, pattern: str) -> List['Path']:
        path_list = self.list_paths_in_partition()
        return [Path(self, path) for path in path_list if fnmatch(path, pattern)]

    def exists(self, path: str) -> bool:
        try:
            detail = self.get_path_details(path)
            return detail['exists']
        except Exception:
            return False

    def open(self, path: str, mode: str = 'r', encoding: Optional[str] = None, errors: Optional[str] = 'strict') -> IO:
        return Path(self, path).open(mode, encoding, errors)

    def __truediv__(self, key):
        return Path(self, key)

class Path:
    def __init__(self, folder: Folder, path: str):
        self.folder = folder
        self.path = str(PurePosixPath(path))
        self._pure_path = PurePosixPath(path)

    def read_bytes(self) -> bytes:
        with self.folder.get_download_stream(self.path) as stream:
            return stream.read()

    def write_bytes(self, data: bytes) -> None:
        self.folder.upload_data(self.path, data)

    def read_text(self, encoding: Optional[str] = None, errors: Optional[str] = 'strict') -> str:
        data = self.read_bytes()
        encoding = encoding or 'utf-8'
        return data.decode(encoding=encoding, errors=errors)

    def write_text(self, data: str, encoding: Optional[str] = None, errors: Optional[str] = 'strict', newline: Optional[str] = None) -> None:
        if not isinstance(data, str):
            raise TypeError(f"入力は文字列である必要があります。受け取った型: {type(data)}")

        encoding = encoding or 'utf-8'

        if newline is not None:
            if newline not in ('', '\n', '\r', '\r\n'):
                raise ValueError("newline must be None, '', '\\n', '\\r', or '\\r\\n'")
            data = data.replace('\n', newline)

        encoded_data = data.encode(encoding=encoding, errors=errors)
        self.write_bytes(encoded_data)

    def imread(self) -> ntp.NDArray:
        buffer = self.read_bytes()
        image = Image.open(BytesIO(buffer))
        return np.array(image)

    def imwrite(self, image: Union[np.ndarray, Image.Image], quality: Optional[int] = None) -> None:
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        if not isinstance(image, Image.Image):
            raise ValueError('入力画像はndarrayまたはPIL画像である必要があります')
        
        format = PurePosixPath(self.path).suffix.lstrip('.')
        if not format:
            raise ValueError('パスは画像形式の分かる拡張子を付けてください')
        
        if format.lower() == 'jpg':
            format = 'jpeg'

        enable_format = [s.lower() for s in Image.SAVE.keys()]
        if format.lower() not in enable_format:
            raise ValueError(f'画像フォーマットは次の中から選択してください: {enable_format}')
        
        save_kwargs = {}
        if format.lower() == 'jpeg' and quality is not None:
            if not 0 <= quality <= 95:
                raise ValueError('qualityは0-95の間で指定してください')
            save_kwargs['quality'] = quality
        
        with BytesIO() as buffer:
            image.save(buffer, format=format, **save_kwargs)
            self.write_bytes(buffer.getvalue())

    def exists(self) -> bool:
        return self.folder.exists(self.path)

    def open(self, mode: str = 'r', encoding: Optional[str] = None, errors: Optional[str] = 'strict') -> IO:
        if mode in ['r', 'rt']:
            return StringIO(self.read_text(encoding, errors))
        elif mode == 'rb':
            return BytesIO(self.read_bytes())
        elif mode in ['w', 'wt']:
            return _WriteTextWrapper(self, encoding, errors)
        elif mode == 'wb':
            return _WriteBytesWrapper(self)
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    @property
    def name(self) -> str:
        return self._pure_path.name

    @property
    def suffix(self) -> str:
        return self._pure_path.suffix

    @property
    def suffixes(self) -> List[str]:
        return self._pure_path.suffixes

    def with_suffix(self, suffix: str) -> 'Path':
        new_path = self._pure_path.with_suffix(suffix)
        return Path(self.folder, str(new_path))

    @property
    def stem(self) -> str:
        return self._pure_path.stem

    def with_stem(self, stem: str) -> 'Path':
        new_path = self._pure_path.with_name(stem + self._pure_path.suffix)
        return Path(self.folder, str(new_path))

    @property
    def parts(self) -> Tuple[str, ...]:
        return self._pure_path.parts

    def with_name(self, name: str) -> 'Path':
        new_path = self._pure_path.with_name(name)
        return Path(self.folder, str(new_path))

    @property
    def parent(self) -> 'Path':
        return Path(self.folder, str(self._pure_path.parent))

    @property
    def parents(self) -> List['Path']:
        return [Path(self.folder, str(parent)) for parent in self._pure_path.parents]
    
    def is_absolute(self) -> bool:
        return self._pure_path.is_absolute()

    def is_relative_to(self, other: Union[str, 'Path']) -> bool:
        if isinstance(other, Path):
            other = other._pure_path
        return self._pure_path.is_relative_to(other)

    def relative_to(self, other: Union[str, 'Path']) -> 'Path':
        if isinstance(other, Path):
            other = other._pure_path
        new_path = self._pure_path.relative_to(other)
        return Path(self.folder, str(new_path))

    def joinpath(self, *other: Union[str, 'Path']) -> 'Path':
        new_path = self._pure_path.joinpath(*[p._pure_path if isinstance(p, Path) else p for p in other])
        return Path(self.folder, str(new_path))
    
    def is_dir(self) -> bool:
        return self.folder.get_path_details(self.path)['directory']

    def is_file(self) -> bool:
        return not self.is_dir()        
    
    def unlink(self) -> None:
        self.folder.delete_path(self.path)
    
    def replace(self, target: Union[str, 'Path']) -> 'Path':
        if isinstance(target, str):
            target = Path(self.folder, target)
        target.write_bytes(self.read_bytes())
        self.unlink()
        return target

    def copy(self, target: Union[str, 'Path']) -> 'Path':
        if isinstance(target, str):
            target = Path(self.folder, target)
        target.write_bytes(self.read_bytes())
        return target

#     # full_match は3.13から
#     def full_match(self, pattern:str) -> bool:
#         return self._pure_path.full_match(pattern)

    def match(self, pattern:str) -> bool:
        return self._pure_path.match(pattern)
            
    def __truediv__(self, key):
        return Path(self.folder, str(PurePosixPath(self.path) / key))

    def __str__(self):
        return self.path

    def __repr__(self):
        return f"Path('{self.path}')"


class _WriteTextWrapper:
    def __init__(self, path, encoding, errors):
        self.path = path
        self.encoding = encoding
        self.errors = errors
        self.buffer = []

    def write(self, data):
        self.buffer.append(data)

    def close(self):
        self.path.write_text(''.join(self.buffer), self.encoding, self.errors)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

class _WriteBytesWrapper:
    def __init__(self, path):
        self.path = path
        self.buffer = BytesIO()

    def write(self, data):
        self.buffer.write(data)

    def close(self):
        self.path.write_bytes(self.buffer.getvalue())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
