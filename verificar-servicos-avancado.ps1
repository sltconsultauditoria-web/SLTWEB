Write-Host ""
Write-Host "====================================="
Write-Host "DIAGNOSTICO AVANCADO DE SERVICOS"
Write-Host "====================================="
Write-Host ""

$portas = @(3000,3001,4000,5000,8000,8001,27017)

foreach ($porta in $portas) {

    Write-Host ""
    Write-Host "Verificando porta $porta..."

    $teste = Test-NetConnection -ComputerName localhost -Port $porta -WarningAction SilentlyContinue

    if ($teste.TcpTestSucceeded) {

        Write-Host "✅ Porta $porta esta ABERTA"

        $linha = netstat -ano | Select-String ":$porta"

        if ($linha) {

            $partes = $linha -split "\s+"

            $processId = $partes[-1]

            $proc = Get-Process -Id $processId -ErrorAction SilentlyContinue

            if ($proc) {

                Write-Host "Processo: $($proc.ProcessName)"
                Write-Host "PID: $processId"

            }

        }

    }
    else {

        Write-Host "❌ Porta $porta fechada"

    }

}

Write-Host ""
Write-Host "====================================="
Write-Host "MAPA DE PORTAS NODE / WEB"
Write-Host "====================================="

netstat -ano | findstr ":3000"
netstat -ano | findstr ":3001"
netstat -ano | findstr ":5000"
netstat -ano | findstr ":8000"
netstat -ano | findstr ":8001"
netstat -ano | findstr ":27017"