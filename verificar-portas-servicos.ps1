Write-Host ""
Write-Host "====================================="
Write-Host "DIAGNOSTICO DE PORTAS DOS SERVICOS"
Write-Host "====================================="
Write-Host ""

# Portas comuns do sistema
$servicos = @(
    @{Nome="Frontend React"; Porta=3000},
    @{Nome="API Gateway"; Porta=3001},
    @{Nome="Backend API"; Porta=5000},
    @{Nome="MongoDB"; Porta=27017}
)

foreach ($s in $servicos) {

    $porta = $s.Porta
    $nome = $s.Nome

    Write-Host ""
    Write-Host "Verificando $nome (porta $porta)..."

    $teste = Test-NetConnection -ComputerName localhost -Port $porta -WarningAction SilentlyContinue

    if ($teste.TcpTestSucceeded) {

        Write-Host "✅ Porta $porta esta ABERTA"

        $processo = netstat -ano | findstr ":$porta"

        if ($processo) {

            $pid = ($processo -split "\s+")[-1]

            $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue

            if ($proc) {
                Write-Host "Processo usando a porta: $($proc.ProcessName) (PID $pid)"
            }

        }

    }
    else {

        Write-Host "❌ Porta $porta esta FECHADA"

    }

}

Write-Host ""
Write-Host "====================================="
Write-Host "PORTAS ABERTAS NO SISTEMA"
Write-Host "====================================="

netstat -ano | findstr LISTENING