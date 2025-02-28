# dataiku-pathlib
A feature to use Dataiku's Managed Folder like a pathlib.

## Folderクラス
このクラスはdataiku.Folderを拡張し、ファイルシステム操作のための追加機能を提供します。

### メソッド

**`glob(pattern: str) -> List['Path']:`**
指定されたパターンに一致するすべてのパスのリストを返します。

**`exists(path: str) -> bool:`**
指定されたパスが存在するかどうかを確認します。

**`open(path: str, mode: str = 'r', encoding: Optional[str] = None, errors: Optional[str] = 'strict') -> IO:`**
指定されたパスのファイルを開きます。

**`__truediv__(key):`**
'/'演算子を使用してPathオブジェクトを生成します。

## Pathクラス
このクラスは、ファイルシステムのパスを表現し、様々なファイル操作メソッドを提供します。

### メソッド
**`__init__(folder: Folder, path: str):`**
Pathオブジェクトを初期化します。

**`read_bytes() -> bytes:`**
ファイルの内容をバイト列として読み込みます。

**`write_bytes(data: bytes) -> None:`**
バイト列をファイルに書き込みます。

**`read_text(encoding: Optional[str] = None, errors: Optional[str] = 'strict') -> str:`**
ファイルの内容をテキストとして読み込みます。

**`write_text(data: str, encoding: Optional[str] = None, errors: Optional[str] = 'strict', newline: Optional[str] = None) -> None:`**
テキストをファイルに書き込みます。

**`read_json() -> Dict:`**
JSONファイルを読み込み、辞書として返します。

**`write_json(object: object):`**
オブジェクトをJSONファイルとして書き込みます。

**`imread() -> ntp.NDArray:`**
画像ファイルを読み込み、NumPy配列として返します。

**`imwrite(image: Union[np.ndarray, Image.Image], quality: Optional[int] = None) -> None:`**
NumPy配列またはPIL画像をファイルに書き込みます。

**`exists() -> bool:`**
パスが存在するかどうかを確認します。

**`open(mode: str = 'r', encoding: Optional[str] = None, errors: Optional[str] = 'strict') -> IO:`**
ファイルを開きます。

**`with_suffix(suffix: str) -> 'Path':`**
新しい拡張子を持つPathオブジェクトを返します。

**`with_stem(stem: str) -> 'Path':`**
新しいステム（拡張子を除いたファイル名）を持つPathオブジェクトを返します。

**`with_name(name: str) -> 'Path':`**
新しい名前を持つPathオブジェクトを返します。

**`is_absolute() -> bool:`**
パスが絶対パスかどうかを確認します。

**`is_relative_to(other: Union[str, 'Path']) -> bool:`**
パスが指定されたパスに対して相対パスかどうかを確認します。

**`relative_to(other: Union[str, 'Path']) -> 'Path':`**
指定されたパスに対する相対パスを返します。

**`joinpath(*other: Union[str, 'Path']) -> 'Path':`**
現在のパスに他のパス要素を結合した新しいPathオブジェクトを返します。

**`is_dir() -> bool:`**
パスがディレクトリかどうかを確認します。

**`is_file() -> bool:`**
パスがファイルかどうかを確認します。

**`unlink() -> None:`**
ファイルを削除します。

**`replace(target: Union[str, 'Path']) -> 'Path':`**
ファイルを移動（名前変更）します。

**`copy(target: Union[str, 'Path']) -> 'Path':`**
ファイルをコピーします。

**`match(pattern:str) -> bool:`**
パスが指定されたパターンにマッチするかどうかを確認します。


### プロパティ
**`name:`**
ファイル名またはディレクトリ名を返します。

**`suffix:`**
ファイルの拡張子を返します。

**`suffixes:`**
ファイルの全ての拡張子のリストを返します。

**`stem:`**
拡張子を除いたファイル名を返します。

**`parts:`**
パスの各要素をタプルとして返します。

**`parent:`**
親ディレクトリのPathオブジェクトを返します。

**`parents:`**
全ての親ディレクトリのPathオブジェクトのリストを返します。

## 使用例

### Folderオブジェクトの作成
```python
from dataiku_pathlib import Folder, Path

# Folderオブジェクトの作成
folder = Folder("sample")
output_folder = Folder("sample_output")

print(repr(folder))
# 出力: <dataiku_pathlib.Folder object at 0x7fbd7858c8b
```

### Folderオブジェクトの操作
```python
# dataiku.Folderを継承しているので、同じメソッドが使える
# フォルダの内容をクリア
output_folder.clear()
```

### ファイルの検索(glob)
```python
# JPGファイルの検索
image_files = folder.glob('*.jpg')
print(image_files)
# 出力: [Path('/4.jpg'), Path('/5.jpg'), Path('/6.jpg'), Path('/a/b/0.jpg'), Path('/sub/1.jpg'), Path('/sub/2.jpg'), Path('/sub/3.jpg')]
```

### ファイルのリネーム
```python
# ファイルのリネーム
for i, file in enumerate(image_files):
    file.replace(file.with_stem(str(i*10)))

image_files = folder.glob('*.jpg')
print(image_files)
# 出力: [Path('/0.jpg'), Path('/10.jpg'), Path('/20.jpg'), Path('/a/b/30.jpg'), Path('/sub/40.jpg'), Path('/sub/50.jpg'), Path('/sub/60.jpg')]
```

### '/'演算子を使用してパスを生成
```python
path1 = folder / "subfolder" / "file.txt"
print(path1)  # 出力: Path('subfolder/file.txt')

path2 = folder / "subfolder/another/file.txt"
print(path2)  # 出力: Path('subfolder/another/file.txt')
```

### 既存のPathオブジェクトから新しいパスを生成
```python
base_path = Path(folder, "base")
new_path = base_path / "subfolder" / "file.txt"
print(new_path)  # 出力: Path('base/subfolder/file.txt')
```

### 文字列から直接Pathオブジェクトを生成
```python
path3 = Path(folder, "direct/path/to/file.txt")
print(path3)  # 出力: Path('direct/path/to/file.txt')
```

### パスの一部を変更
```python
path4 = path3.with_name("newfile.txt")
print(path4)  # 出力: Path('direct/path/to/newfile.txt')
```

### 拡張子の変更
```python
path5 = path4.with_suffix(".csv")
print(path5)  # 出力: Path('direct/path/to/newfile.csv')
```

### 親ディレクトリの取得
```python
parent = path5.parent
print(parent)  # 出力: Path('direct/path/to')
```

### 画像の読み込み
```python
image_path = folder / "0.jpg"
image_array = image_path.imread()

print(type(image_array))  # 出力: <class 'numpy.ndarray'>
print(image_array.shape)  # 出力: (height, width, channels)
```

### 画像の書き込み
```python
# NumPy配列から画像を保存
output_path = output_folder / "output.png"
output_path.imwrite(image_array)

# 別の形式で保存（JPEGの場合、品質も指定可能）
jpeg_path = output_folder / "output.jpg"
jpeg_path.imwrite(image_array, quality=95)
```
