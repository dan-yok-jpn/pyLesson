VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "QuadFnc"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False

Private self_a As Double
Private self_b As Double
Private self_c As Double

Function f(x)
    f = (self_a * x + self_b) * x + self_c
End Function

Sub init(a, b, c)
    self_a = a
    self_b = b
    self_c = c
End Sub

Sub solve(ByRef sols)
    ReDim sols(1)
    If self_a = 0 Then
        er = CVErr(xlErrNA)
        sols(0) = er
        sols(1) = er
        Return
    End If
    dd = self_b ^ 2 - 4 * self_a * self_c
    If dd >= 0 Then
        d = Sqr(dd)
        a2 = self_a * 2
        sols(0) = (-self_b - d) / a2
        sols(1) = (-self_b + d) / a2
    Else ' give up treating complex number
        MsgBox "There is no solution of real number"
        er = CVErr(xlErrNA)
        sols(0) = er
        sols(1) = er
    End If
End Sub

Function str_()
    If self_b > 0 Then cb = "+" Else cb = ""
    If self_c > 0 Then cc = "+" Else cc = ""
    str_ = "f(x)=(" & Trim(Str(self_a)) & "x"
    str_ = str_ & cb & Trim(Str(self_b)) & ")x"
    str_ = str_ & cc & Trim(Str(self_c))
End Function

Sub plot(xmin, xmax, xdiv)
    n = Int((xmax - xmin) / xdiv)
    xdiv = (xmax - xmin) / n
    XValues = "{" & Str(xmin)
    YValues = "{" & Str(Me.f(xmin))
    For i = 1 To n
        x = xmin + i * xdiv
        XValues = XValues & "," & Str(x)
        YValues = YValues & "," & Str(Me.f(x))
    Next
    XValues = XValues & "}"
    YValues = YValues & "}"
    With ActiveSheet.Shapes.AddChart.Chart
        .ChartType = xlXYScatterLinesNoMarkers
        .HasTitle = True
        .ChartTitle.Text = Me.str_()
        .HasLegend = False
        With .SeriesCollection.NewSeries
            .XValues = XValues
            .Values = YValues
        End With
        With .Axes(xlCategory)
            .MinimumScale = xmin
            .MaximumScale = xmax
            .CrossesAt = xmin
            .HasMajorGridlines = True
        End With
        With .Axes(xlValue)
            .CrossesAt = .MinimumScale
        End With
    End With
End Sub

