# Script para gerar o site localmente sem travar o pre-commit
Write-Host "Iniciando Build do Hugo..." -ForegroundColor Cyan
npx --yes hugo-bin --gc --minify --destination static
Write-Host "Build concluído! O site foi gerado na pasta 'static/'." -ForegroundColor Green
