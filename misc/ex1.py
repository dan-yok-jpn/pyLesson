
'''
サーチパスから Python に関係するものを抽出する 
'''
import os

syoshinsya = True

if syoshinsya:

    moji = os.environ["PATH"]

    hairetsu = moji.split(";")
    yoso_su = len(hairetsu)

    for i in range(yoso_su):

        yoso = hairetsu[i]
        YOSO = yoso.upper()
        gaito = "PYTHON" in YOSO
        if gaito == True:
            print(yoso)
        else:
            hi_gaito = yoso

    renban_hassei_ki = range(yoso_su)
    renban = list(renban_hassei_ki)
    pass

else:
    for Path in os.environ["PATH"].split(";"):
        if "PYTHON" in Path.upper():
            print(Path)

''' VBA の場合
Private Sub CommandButton1_Click()
    r = 1
    Paths = Split(Environ("PATH"), ";")
    For Each Path In Paths
   'For i = 0 To UBound(Paths) : Path = Paths(i)
        If InStr(UCase(Path), "PYTHON") Then
            Cells(r, 1) = Path : r = r + 1
        End If
    Next
End Sub
'''