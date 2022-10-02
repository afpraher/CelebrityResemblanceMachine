
Write-Host "----------------------------------"
Write-Host "Extracting Images"
Write-Host "----------------------------------"
Expand-Archive .\Celebs.zip .\

Write-HOst "----------------------------------"
Write-Host "Installing dependencies"
Write-HOst "----------------------------------"
python.exe -m pip install --user wheel argparse matplotlib numpy opencv-python pillow face_recognition tqdm

Write-Host "----------------------------------"
Write-Host "Done"
Write-Host "Press key to continue"

[System.Console]::ReadKey()