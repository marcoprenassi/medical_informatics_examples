# Medical Informatics Examples

Public repository of examples and snippets of code (made largely by me) dedicated to medical informatics

1. UMLS_Api_search_example:  
 UMLS ([link](https://www.nlm.nih.gov/research/umls/index.html)) REST API ([link](https://documentation.uts.nlm.nih.gov/rest/home.html))
simple search and retrieve app with a basic graphical UI (PySimpleGUI).  
Requires:  
    - requests, json and datetime modules, 
    - beatifulsoup (bs4), pandas, tabulate,
    - PySimpleGUI for the graphical interface
    - also the UMLS personal API Key ([link](https://documentation.uts.nlm.nih.gov/rest/authentication.html)):
      
    1. Quickstart  
       import UMLS_Api_search_example as UAex  
       UAex.runExample("[INSERT API KEY HERE]")  
       

