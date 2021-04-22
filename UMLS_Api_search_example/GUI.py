"""
Created on Mon Apr 22 11:25:00 2021

@author: marcoprenassi
"""

import PySimpleGUI as PyGUI


def GUI(UMLSAPIObject):
    PyGUI.theme('DarkGrey9')  # Add a touch of color

    # All the stuff inside your window.
    # noinspection PyTypeChecker
    layout = [[PyGUI.Text('UMLS search')],
              [PyGUI.Text('Enter the search term: '), PyGUI.InputText()],
              [PyGUI.Button('Search'), PyGUI.Button('Exit')],
              [PyGUI.Table(['', '', '', ''], key='results', headings=['ui', 'rootSource', 'uri', 'name'],
                           col_widths=[10, 15, 45, 45], justification='left', auto_size_columns=False)]]

    PyGUI.set_options(element_padding=(0, 0))

    # Create the Window
    window = PyGUI.Window('UMLS Search', layout, return_keyboard_events=True)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == PyGUI.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
            break
        elif event == 'Search' or event == '\r':
            UMLSAPIObject.search(search_term=values[0])
            window['results'].update(UMLSAPIObject.result_list_dataframe[0:].values.tolist())
    window.close()
