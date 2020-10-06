# Perform the code-generation step for this example application.
if ( $env:AMBVARIANT ) {
    $AMBVARIANT = $env:AMBVARIANT
} else {
    $AMBVARIANT="x64\Debug\net46"
}

if ( $env:AMBVARIANTCORERELEASE ) {
    $AMBVARIANTCORERELEASE=$env:AMBVARIANTCORERELEASE
} else {
    $AMBVARIANTCORERELEASE = "x64\Release\netcoreapp3.1"
}

if ( $env:AMBROSIATOOLS ) {
    $AMBROSIATOOLS=$env:AMBROSIATOOLS
} else {
    $AMBROSIATOOLS = "..\..\Clients\CSharp\AmbrosiaCS\bin"
}

Write-Host "Using variant of AmbrosiaCS: $AMBVARIANT"

# Generate the assemblies, assumes an .exe which is created by a .Net Framework build:
Write-Host "Executing codegen command: $AMBROSIATOOLS\$AMBVARIANT\AmbrosiaCS.exe CodeGen -a=NodeAPI\bin\$AMBVARIANT\IServer.dll -p=NodeAPI\IServer.csproj -o=ServerInterfaces -f=net46 -f=netcoreapp3.1"
& $AMBROSIATOOLS\$AMBVARIANT\AmbrosiaCS.exe CodeGen -a="NodeAPI\bin\$AMBVARIANT\IServer.dll" -p="NodeAPI\IServer.csproj" -o=NodeInterfaces -f="net46" -f="netcoreapp3.1"


