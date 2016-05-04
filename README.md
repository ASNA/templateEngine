### An Amyuni PDF wrapper library
   
The Amyuni PDF driver needs several configuration tasks performed before it can be used. To make the Amyuni PDF driver easy to use we've squirreled away these tasks in a simple AVR class library wrapper composed of three classes: 

* __Helpers__ provides a couple of helper methods.  
* __PdfDriverInfo__ provides driver and runtime properties. Once these properties are populated, all of the data needed the use the Amyuni PDF driver is available in a single place. This class populates some of the driver properties from an XML file (more on this in a moment) and it also provides a shared `GetInstance()` factory (of sorts) method to return an instance of itself. This factory method encapsulates  all of the smarts to instance the `DriverInfo` class. This class instance is available as the `DriverInfo` property of the `Manager` class.      
* __Manager__ provides the methods that empower the Amyuni PDF driver to do its magic. The three methods (which correspond nearly directly to the three Amyuni APIs needs to work with the driver) are:
	* __StartDriver__ is a subroutine that starts the Amyuni PDF driver. After calling this method, the driver is ready to accept output. 
	* __StopDriver__  is a function that stops the Amyuni PDF driver. This method must be called after the report logic has been performed. This driver stops the Amyuni PDF driver and returns the PDF's file name (the name and extension only, not the file's fully qualified path location).  git sta
     
These classes all live within the ASNA.AmyuniPDF namespace. Most of the code in this project is either self-explanatory or can be looked up in the [Amyuni documentation](https://www.amyuni.com/WebHelp/Developer_Documentation.htm#Amyuni_Document_Converter/Introduction.htm).  

#### Persisting runtime values   

When you purchase the Amuni PDF driver you are provided a runtime license code and the exact company name for whom the license was issued. You'll also need to know, at runtime, the name of the Amyuni PDF virtual printer (this is the name of the printer you see when you work with printers and devices). In this example that printer was named `AmyuniPDFConverter`. For safe keeping and easy access, these values are persisted in an XML file named `AmyuniDriverInfo.XML`. This was Forrest's idea and it's a great one. The `GetInstance()` method of the `ASNA.AmyuniPDF.DriverInfo` class parses this XML file to populate driver properties.    
 
	<?xml version="1.0" encoding="utf-8" ?>
	<Root>
	    <AmyuniPDF>
	        <PrinterName>AmyuniPDFConverter</PrinterName>
	        <LicenseCompany>Amyuni Tech Eval</LicenseCompany>
	        <LicenseCode>07EFCDAB01...</LicenseCode>
	    </AmyuniPDF>
	</Root>

#### Runtime properties

The following properties are surfaced by the `DriverInfo` class:

* __PrinterName__ Populated from the `AmyuniDriverInfo.XML` file.
* __LicenseCompany__ Populated from the `AmyuniDriverInfo.XML` file.
* __LicenseCode__ Populated from the `AmyuniDriverInfo.XML` file.
* __OutputPath__ Provided at runtime. 
* __OutputFileName__ This is a short, randomly-generated file name without the `.pdf` extension&mdash;it gets added later. This file is generated with the `System.IO.Path.GetRandomFileName()` method. Beyond providing the core part of the PDF file name this is also the name of the entry in the Windows print spooler.  

#### Referencing the Amyuni ActiveX COM object

This class library needs a reference to the Amyuni Document Converter ActiveX COM object. To set this, right click on your solution and click "Add reference..." Then, click the COM tab and scroll down to the Amyuni ActiveX component and click "OK." 

![](https://asna.com/filebin/marketing//article-figures/SetAmyuniReference.png?x=1449611644571)

When you add a reference to a COM object in .NET, what you really need is the `Interop` version of the DLL (which is a .NET assembly that provides .NET with runtime type information about the COM component). That doesn't appear in the BIN folder when you add a COM reference to class library. In consuming Windows or Web apps, we'll also add a reference to the Amyuni ActiveX component and that will provide those projects' BIN folder with the necessary `Interop` version of the DLL.

#### Example usage

The simplest possible use of this class library is shown below. In this case, `XmlFilePath` provides the path where the `AmyuniDriverInfo.XML` is located and `OutFilePath` is the output path where you want generated PDFs placed.


    DclPrintFile MyPrint +
                 DB(prntDB) +
                 File("Examples/CustList2") +
                 ImpOpen(*No)	

    DclFld am          Type(ASNA.AmyUniPDF.Manager)
    DclFld PDFFileName Type(*String)

    am = *New ASNA.AmyUniPDF.Manager(XmlFilePath, OutputFilePath)
    am.StartDriver()
    MyPrint.Printer = am.DriverInfo.PrinterName
    MyPrint.ReportName = am.DriverInfo.OutputFileName

    PrintReport()

    PDFFileName = am.StopDriver()
    
After calling `StartDriver()`, it's very important to assign the `PrinterName` and the `OutputFileName` properties to the DataGate printer file's `Printer` and `ReportName` properties (respectively).

The PrintReport() provides the logic to write to formats of the DataGate print file. There isn't anything Amyuni PDF driver-specific in that logic.

Error handling is all exception based. Handling any thrown exceptions is omitted from the the example code below.    

#### Waiting for output

Most of the code in the `Manager` class's StartDriver() and StopDriver() methods is pretty predictable, especially if you look at the [Amyuni docs](https://www.amyuni.com/WebHelp/Developer_Documentation.htm#Amyuni_Document_Converter/Introduction.htm). There is, however, one thing that deserves mentioning that occurs in the `Manager` classe's `StopDriver()` method (its code is shown below). 

    BegFunc StopDriver Type(*String) Access(*Public)
        DclFld SpoolFileName Type(*String)

        SpoolFileName = DriverInfo.OutputFileName
        AmyuniPDF.RestoreDefaultPrinter()
        AmyuniPDF.Unlock(SpoolFileName, 1000)
        AmyuniPDF.DriverEnd()
        AmyuniPDF = *Nothing

        WaitForFile(DriverInfo.OutputPath + DriverInfo.OutputFileName + ".pdf")
        LeaveSr DriverInfo.OutputFileName + ".pdf"
    EndFunc

This method should be called after your logic has printed your report. You'll notice that this code calls the Amyuni PDF driver's `Unlock()` method. This call is a little on the superstitious side because the driver itself calls this method internally when it's needed. The Unlock() method unlocks the given spool file name and then waits a given number of milliseconds to ensure the PDF is written and closed before continuing. However, you'll also notice a that a second wait occurs in the WaitForFile method (that method is in the `Manager` class). That code provides a second test to make absolutely sure the PDF is ready to use. Latency can occur as the PDF is being written disk and this avoids any problems that may cause.