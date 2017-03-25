#!/home/cori/anaconda3/bin/python
import inspect


#------------------------------------------------------------------------------
def set_verbosity(verbosity):
  global verbosity_level
  verbosity_level = 3
  if verbosity == 'HIGH':
    verbosity_level = 0
  elif verbosity == 'MEDIUM':
    verbosity_level = 1
  elif verbosity == 'LOW':
    verbosity_level = 2
  elif verbosity == 'OFF':
    verbosity_level = 3
  return

#------------------------------------------------------------------------------
def lineno():
  """Returns the current line number in our program."""
  return inspect.currentframe().f_back.f_lineno

#------------------------------------------------------------------------------
def hook(calling_file, status, verbosity, line_number, message):
  """ writes out a status message based on the line number and the status level """
  """ The status level can be INFO, WARNING or ERROR """
  # Example
  # hook("HIP_shuffle.py", "ERROR", "LOW", lineno(), "Could not get lib name and version: {}".format(lib_and_version))
  # -------------------
  hook_padding_spaces = ""
  if (line_number < 1000):
    hook_padding_spaces = " "
  if (line_number < 100):
    hook_padding_spaces = "  "
  if (line_number < 10):
    hook_padding_spaces = "   "
  # -------------------
  verbosity_number = 3
  if (verbosity == "HIGH"):
    verbosity_number = 0
  if (verbosity == "MEDIUM"):
    verbosity_number = 1
  if (verbosity == "LOW"):
    verbosity_number = 2
  if (verbosity == "OFF"):
    verbosity_number = 3
  # -------------------
  if (status == "INFO" and (verbosity_number >= verbosity_level)):
    print("[INFO    " + hook_padding_spaces + str(line_number) + " (" + calling_file  + ")]: " + message)
  if (status == "WARNING"):
    print("[WARNING " + hook_padding_spaces + str(line_number) + " (" + calling_file  + ")]: " + message)
  if (status == "ERROR"):
    print("[ERROR   " + hook_padding_spaces + str(line_number) + " (" + calling_file  + ")]: " + message)
  if (status == "FATAL"):
    sys.exit("[FATAL   " + hook_padding_spaces + str(line_number) + " (" + calling_file  + ")]: " + message)