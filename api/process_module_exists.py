import sys, traceback;

modulename = sys.argv[1];
name = sys.argv[1];
try:
    module = __import__(modulename, globals(), locals(  ), [name])
except:
    print('Não existe modulo: ', modulename);
    exit(1);