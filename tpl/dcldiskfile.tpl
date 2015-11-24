    DclDB pgmDB DBName("*PUBLIC/DG NET Local")

    DclDiskFile {{ ProgramName }} +
          Type(*Input) +
          Org(*Indexed) +
          Prefix({{ ProgramName }}_) +
          File("*Libl/{{ FileName  }}") +
          DB(pgmDB) +
          ImpOpen(*No)