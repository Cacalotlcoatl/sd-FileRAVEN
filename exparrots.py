def error_handler(errorcode, error):
    # Exit the program if the error is fatal. Otherwise, print a warning.
    if errorcode > 999:
        with open('error.log', 'w') as logfile:
            logfile.write('ERRORCODE: ' + str(errorcode) + ' ' + str(error))
        print('fileRAVEN has encountered a fatal error and '
              'terminated\nERRORCODE: ', errorcode, error)
        exit()
    else:
        # pop a warning if the error is non-fatal
        print('fileRAVEN has encountered an error: \nERRORCODE: ', errorcode,
              error)
        return ()

# Error Codes
# ----------------------------------------------------------------
# |Code|Error Description|Notes|
# |----|-----------------------------------------|-----------------------------|
# |100|File not found||
# |101|Model information File not found||
# |1000|Fatal Error||
