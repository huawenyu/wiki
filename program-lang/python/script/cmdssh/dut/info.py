
class DutType:
    # static member
    Dummy, Linux, DutKVM, DutFOS, DutFPX, DutNone = range(6)

    dictType = {
        Dummy: "Dummy",
        Linux: "Linux",
        DutKVM: "DutKVM",
        DutFOS: "DutFOS",
        DutFPX: "DutFPX",
        DutNone: "DutNone",
    }

    dictEcho = {
        Dummy: "echo",
        Linux: "echo",
        DutKVM: "sysctl echo",
        DutFOS: "sysctl echo",
        DutFPX: "sysctl echo",
    }

    def __init__(self, name, osType, debugVer):
        self.name = name
        self.osType = osType
        self.debugVer = debugVer

    def __str__(self):
        """
        >>> dut = DutType("DutFOS01", DutType.DutFOS, True)
        >>> print(dut)
        [DutFOS01] is DutFOS (Debug)
        >>> dut = DutType("DutFOS-dummy", 10, False)
        >>> print(dut)
        [DutFOS-dummy] is nothing (Release)
        """
        return "[%s] is %s (%s)" % (self.name, DutType.dictType.get(self.osType, "nothing"), "Debug" if self.debugVer else "Release")

    def echoStr(self):
        """
        >>> dut = DutType("DutFOS02", DutType.DutFOS, False)
        >>> dut.echoStr()
        'fnsysctl echo'
        >>> dut = DutType("DutFOS02", DutType.DutFOS, True)
        >>> dut.echoStr()
        'sysctl echo'
        """

        if self.osType == DutType.Linux:
            return self.dictEcho.get(self.osType, "echo")
        return self.dictEcho.get(self.osType, "echo") if self.debugVer else "fn" + DutType.dictEcho.get(self.osType, "echo")


class DutInfo:
    def __init__(self, name):
            self.Name          = name
            self.Prompt        = ''

            self.Product       = "FortiGate"
            self.Model         = "Linux"
            self.Version       = "0"
            self.VerNum        = 0
            self.VerNum2       = 0
            self.BuildNum      = "0"
            self.BuildDate     = "0"
            self.ModelSN       = "Linux"
            self.LogDisk       = "Available"
            self.Hostname      = "Linux"
            self.OperationMode = "NAT"
            self.Vdom          = "disable"
            self.HAmode        = "standalone"
            self.SystemTime    = "0"


    def __str__(self):
        return (f"{self.Name} info:\n"\
                f"    Product={self.Product} Model={self.Model} Version={self.Version} VerNum={self.VerNum} BuildNum={self.BuildNum} {self.BuildDate}\n"\
                f"    Hostname={self.Hostname} ModelSN={self.ModelSN}\n"\
                f"    LogDisk={self.LogDisk} OperationMode={self.OperationMode} Vdom={self.Vdom} HAmode={self.HAmode}")

    def has_vdom(self):
        return False if self.Vdom == "disable" else True

