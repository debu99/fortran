PROGRAM cmdlnsum
IMPLICIT NONE
CHARACTER(100) :: str1, str2, text

!First, make sure the right number of inputs have been provided
IF(COMMAND_ARGUMENT_COUNT().NE.2)THEN
  WRITE(*,*)'ERROR, TWO COMMAND-LINE ARGUMENTS REQUIRED, STOPPING'
  STOP
ENDIF

CALL GET_COMMAND_ARGUMENT(1,str1)   !first, read in the two values
CALL GET_COMMAND_ARGUMENT(2,str2)

print "(A, A, X, A, X, A)", '#', TRIM(str1), TRIM(str2), 'Column3'
print "(A, X, A, X, A)", '123', '456', '5234'
print "(A, X, A, X, A)", '4555', '456', '23'
print "(A, X, A, X, A)", '1', '4563', '23434'

END PROGRAM