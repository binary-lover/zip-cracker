# zip cracker

## Description
This is a simple zip cracker that uses a `dictionary attack` to crack the password of a zip file. The program reads a dictionary file and tries each word as a password to extract the contents of the zip file. The program is written in Python and uses the zipfile module to extract the contents of the zip file.

## requirements
- Python 3.x
- zipfile module
- rarfile module
- 7z installed on the system


## Usage

```bash
python zip_cracker.py -p <zip_file> -w <dictionary_file>
```

## Example

```bash
python zip_cracker.py -p test.zip -w dictionary.txt
```
