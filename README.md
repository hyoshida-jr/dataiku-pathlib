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
