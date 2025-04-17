from cx_Freeze import setup, Executable # type: ignore
setup(
    name="ECLA timer",
    version="1.0",
    description="Minuterie simple pour ECLA créée par ISSA MOEVA Aïssa",
    executables=[Executable("Minuterie.py", base="Win32GUI", icon="ECLA-Timer.ico")]
)