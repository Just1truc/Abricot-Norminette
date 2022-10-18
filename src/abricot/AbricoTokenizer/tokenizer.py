## Local imports
from typing import Union
from abricot.AbricoTokenizer.custom_exceptions import TokensError, PreprocessingError, UnknownTokenError
from abricot.AbricoTokenizer.custom_types import PCPPToken, ParsingOptions, TokenObject, TokenSequence
from program.abriThread import Abrifast
import os
from abricot.AbricoTokenizer.logger import log_service
## Remote imports
from pcpp import Preprocessor

log : bool = False
logSave : bool = False

if (log):
    AbriLogger = log_service(logSave)


def filterTokens(FilterSequence : list[str], tokenList : TokenSequence, parsingOptions : ParsingOptions) -> list[str]:
    filteredTokenSequence : TokenSequence = TokenSequence([])

    for token in tokenList:
        if token.type not in FilterSequence:
            continue
        if token.line < parsingOptions.fromLine:
            continue
        if token.line == parsingOptions.fromLine and token.column < parsingOptions.fromColumn:
            continue
        if parsingOptions.toLine != -1 and token.line > parsingOptions.toLine:
            continue
        if parsingOptions.toColumn != -1 and token.line == parsingOptions.toLine and token.cur_column > parsingOptions.toColumn:
            continue
        filteredTokenSequence.append(token)

    return filteredTokenSequence 


## Get Token From File name ##
def getTokens(FileName : str, fromLine : int, fromColumn : int, toLine : int, toColumn : int, FilterSequence : list[str]):

    ## Args check

    if (fromLine < 1 or fromColumn < 0 or (toLine > 0 and fromLine > toLine) or (fromLine == toLine and toColumn >= 0 and fromColumn > toColumn)):
        raise TokensError('illegal range of tokens requested by the script')
    
    parsOpt : ParsingOptions = ParsingOptions(fromLine=fromLine, fromColumn=fromColumn, toLine=toLine, toColumn=toColumn)

    return filterTokens(FilterSequence=FilterSequence, tokenList=TokenizerObject.getTokens(FileName), parsingOptions=parsOpt)


#Instancier l'objet et faire une méthode setFile qui initialise les files. 
class Tokenizer():

    def __init__(self):
        if (log):
            print(AbriLogger.info('>> Tokenizer.__init__'))

        self.abriThread = Abrifast()

        self.fileList : list[str] = []
        self.tokensPerFile : dict[str, TokenSequence] = {}
        self.concat_type : dict[str, str] = {
            "HAT,EQUAL" : "xorassign",
            "DOT,DOT,DOT" : "ellipsis",
            "INTEGER,DOT,INTEGER" : "floatlit"
        }
        self.pp_values : dict[str, str] = {
            "define" : "pp_define",
            "if" : "pp_if",
            "if" : "pp_if",
            "ifdef" : "pp_ifdef",
            "ifndef" : "pp_ifndef",
            "else" : "pp_else",
            "elif" : "pp_elif",
            "endif" : "pp_endif",
            "error" : "pp_error",
            "line" : "pp_line",
            "pragma" : "pp_pragma",
            "undef" : "pp_undef",
            "warning" : "pp_warning",
            "include" : "pp_include"
        }

        self.type_dict = {
            "asm": "asm",
            "auto": "auto", 
            "bool": "bool",
            "false": "false", 
            "true": "true", 
            "break": "break", 
            "case": "case", 
            "catch": "catch",
            "char": "char",
            "class": "class",
            "const": "const", 
            "continue": "continue",
            "default": "default",
            "delete": "delete",
            "do": "do",
            "double": "double",
            "else": "else",
            "enum": "enum",
            "explicit": "explicit",
            "export": "export",
            "extern": "extern",
            "float": "float",
            "for": "for",
            "goto": "goto",
            "if": "if",
            "inline": "inline",
            "int": "int",
            "long": "long",
            "mutable": "mutable",
            "namespace": "namespace",
            "new": "new",
            "operator": "operator",
            "private": "private",
            "protected": "protected",
            "public": "public",
            "register": "register",
            "return": "return",
            "short": "short",
            "signed": "signed",
            "sizeof": "sizeof",
            "static": "static",
            "struct": "struct",
            "switch": "switch",
            "template": "template",
            "throw": "throw",
            "try": "try",
            "typedef": "typedef",
            "typeid": "typeid",
            "typename": "typename",
            "union": "union",
            "unsigned": "unsigned",
            "using": "using",
            "virtual": "virtual",
            "void": "void",
            "volatile": "volatile",
            "wchart": "wchart", 
            "while": "while",
            "any": "any"
        }

        self.type2vera_type = {
            "ID" : "identifier",
            "AMPERSAND": "and",
            "LOGICALAND": "andand",
            "EQUAL": "assign",
            "ANDEQUAL": "andassign",
            "BAR": "or",
            "OREQUAL": "orassign",
            "HAT": "xor",
            "COMMA": "comma",
            "COLON": "colon",
            "FSLASH": "divide",
            "DIVIDEEQUAL": "divideassign",
            "DOT": "dot",
            "EQUALITY": "equal",
            "GREATER": "greater",
            "GREATEREQUAL": "greaterequal",
            "LCURLY": "leftbrace",
            "LESS": "less",
            "LESSEQUAL": "lessequal",
            "LPAREN": "leftparen",
            "LBRACKET": "leftbracket",
            "MINUS": "minus",
            "MINUSEQUAL": "minusassign",
            "MINUSMINUS": "minusminus",
            "PERCENT": "percent",
            "PERCENTEQUAL": "percentassign",
            "EXCLAMATION": "not",
            "INEQUALITY": "notequal",
            "LOGICALOR": "oror",
            "PLUS": "plus",
            "PLUSEQUAL": "plusassign",
            "PLUSPLUS": "plusplus",
            "DEREFERENCE": "arrow",
            "QUESTION": "question_mark",
            "RCURLY": "rightbrace",
            "RPAREN": "rightparen",
            "RBRACKET": "rightbracket",
            "SEMICOLON": "semicolon",
            "LSHIFT": "shiftleft",
            "LSHIFTEQUAL": "shiftleftassign",
            "RSHIFT": "shiftright",
            "RSHIFTEQUAL": "shiftrightassign",
            "STAR": "star",
            "MULTIPLYEQUAL": "starassign",
            "COMMENT1": "ccomment",
            "COMMENT2" : "cppcomment",
            "CHAR": "charlit",
            "STRING": "stringlit",
            "DPOUND": "pound_pound",
            "POUND": "pound",
            "INTEGER" : "intlit",
            "WS" : "space"
        }

        if (log):
            print(AbriLogger.info('<< Tokenizer.__init__'))


    def setFiles(self, filePathList : list[str]):
        if (log):
            print(AbriLogger.info('>> Tokenizer.setFiles'))
        self.fileList = filePathList
        self.initAllFilesTokens()
        if (log):
            print(AbriLogger.info('<< Tokenizer.setFiles'))


    def check_isNL(sencalf, token : TokenObject) -> bool:
        """ Check if token is a new line or a simple ws """
        return token.type == 'CPP_WS' and token.value == '\n'

    def checkConcatType(self, tokenIndex : int, pcppTokens : list[PCPPToken]) -> Union[tuple[str, str], bool]:
        """ Check if a type is a combinaison of multiple characters not checked by pcpp """
        if (log):
            print(AbriLogger.info('>> Tokenizer.checkConcatType'))

        for ct in self.concat_type:

            pcppTokensListSize : int = len(pcppTokens)

            types : list[str] = ct.split(',')
            i = 0
            while i < len(types) and tokenIndex + i + 1 < pcppTokensListSize and pcppTokens[tokenIndex + i].type == f'CPP_{types[i]}':
                i += 1

            if i == len(types):
                if (log):
                    print(AbriLogger.success('<< Tokenizer.checkConcatType : Success'))

                res : list[str] = [self.concat_type[ct], pcppTokens[tokenIndex].value]
                u = 1
                while (u < len(types)):
                    res[1] = res[1] + pcppTokens[tokenIndex + 1].value
                    pcppTokens.pop(tokenIndex + 1)
                    u += 1
                return tuple(i for i in res)

        if (log):
            print(AbriLogger.info('<< Tokenizer.checkConcatType'))
        return False


    def getHheader(self, pcppTokens : list[PCPPToken], tokenIndex : int) -> bool:
        """ check if import is part given with include """
        return tokenIndex + 5 < len(pcppTokens) and (
            (pcppTokens[tokenIndex + 1].value == '<' and pcppTokens[tokenIndex + 5].value == '>')
            ) and pcppTokens[tokenIndex + 3].value == '.'


    def checkPPValues(self, tokenIndex : int, pcppTokens : list[PCPPToken]) -> Union[tuple[str, str], bool]:
        """ Test if types are preprocessors types """
        if (log):
            print(AbriLogger.info('>> Tokenizer.checkPreProcessorValues'))

        if (pcppTokens[tokenIndex].type != 'CPP_POUND' or tokenIndex + 1 > len(pcppTokens)):
            return False

        for PreProcessorValues in self.pp_values:
            if (pcppTokens[tokenIndex + 1].value == PreProcessorValues):
                if (log):
                    print(AbriLogger.success('<< Tokenizer.checkPreProcessorValues : Value found'))

                concat_values : int = 2
                
                if pcppTokens[tokenIndex + 1].value == 'include' and tokenIndex + 2 < len(pcppTokens) and pcppTokens[tokenIndex + 2].type == 'CPP_WS':
                    concat_values = 3
                if (tokenIndex + 3 < len(pcppTokens) and pcppTokens[tokenIndex + 3].type == 'CPP_STRING'):
                    concat_values = 4
                if self.getHheader(pcppTokens=pcppTokens, tokenIndex=tokenIndex + 2):
                    concat_values = 8

                if (log):
                    print(AbriLogger.info(f'Concat value : {concat_values}'))
                
                tpl : tuple[str, str] = (('pp_hheader' if pcppTokens[tokenIndex + 3].value == '<' else 'pp_qheader') if concat_values == 8 or concat_values == 4 else self.pp_values[PreProcessorValues], ''.join([token.value for token in pcppTokens[tokenIndex: tokenIndex + concat_values]]))

                del pcppTokens[tokenIndex: tokenIndex + concat_values]

                return tpl
        
        if (log):
            print(AbriLogger.info('<< Tokenizer.checkPreProcessorValues'))
        return False


    def initTokens(self, filePath : str) -> TokenSequence:

        if (log):
            print(AbriLogger.info('>> Tokenizer.initTokens'))
        if not any([filePath.endswith(ext) for ext in ['.c', '.h']]) and not filePath.endswith('Makefile'):
            return []
        file_content : str = open(filePath, mode='r', encoding='utf-8', errors="ignore").read()

        try:
            list_pcppTokens : list = Preprocessor().tokenize(text=file_content)
            pcpp_tokens : list[PCPPToken] = []
            for token in list_pcppTokens:
                pcpp_tokens.append(PCPPToken(value=token.value, lineno=token.lineno - 2, lexpos=token.lexpos, type=token.type, source=token.source))

        except:
            if (log):
                print(AbriLogger.error('Error while getting tokens from pcpp'))
            raise PreprocessingError()

        if (log):
            print(AbriLogger.success('>> Tokenizer.initTokens : Successfully got tokens from pcpp'))

        ret : TokenSequence = TokenSequence([])

        #get tokens
        line : int = 1
        column_offset : int = 0
        base_offset : int = 0

        for index, pcppToken in enumerate(pcpp_tokens):

            #check types, new element ect

            tokenRef : TokenObject = TokenObject(file=filePath, column=pcppToken.lexpos, line=pcppToken.lineno, type=pcppToken.type, raw=pcppToken.source, value=pcppToken.value, cur_column=pcppToken.lexpos)
    
            # Get new line number and setup column offset

            if (tokenRef.line > line):
                line = tokenRef.line
                column_offset = file_content[:tokenRef.column].rfind('\n') + 1

            base_offset = tokenRef.column
            tokenRef.column = base_offset - column_offset

            if (self.check_isNL(tokenRef) == True):
                tokenRef.raw = '\n'
                tokenRef.type = 'newline'
                tokenRef.name = tokenRef.type
                ret.append(item=tokenRef)
                continue

            # Check types composed of multiple tokens 
            concatTypeResult : Union[str, bool] = self.checkConcatType(tokenIndex=index, pcppTokens=pcpp_tokens)
            if (concatTypeResult != False):
                tokenRef.type = concatTypeResult[0]
                tokenRef.value = tokenRef.raw = concatTypeResult[1]
                tokenRef.name = tokenRef.type
                ret.append(item=tokenRef)
                continue

            ## Check if type is preprocessing type
            PPTypeTest : Union[tuple[str, str], bool] = self.checkPPValues(tokenIndex=index, pcppTokens=pcpp_tokens)
            if (PPTypeTest != False):
                tokenRef.type = PPTypeTest[0]
                tokenRef.value = PPTypeTest[1]
                tokenRef.raw = PPTypeTest[1]
                tokenRef.name = tokenRef.type
                ret.append(item=tokenRef)
                continue

            ## check if type is a specific type
            if (tokenRef.value in self.type_dict):
                tokenRef.type = self.type_dict[tokenRef.value]
                tokenRef.name = tokenRef.type
                ret.append(item=tokenRef)
                continue

            # Setup type for classic types
            tokenRef.type = self.type2vera_type.get(tokenRef.type.replace('CPP_', ''))

            tokenRef.name = tokenRef.type
            #line = tokenRef.line if tokenRef.line > line else line

            ret.append(item=tokenRef)

        # todo améliorer la position de l'eof
        ret.append(TokenObject(file=filePath, column=0, line=line + 1, name='eof', type='eof', raw='', value=''))

        #end get tokens

        return ret

    def directAdd(self, filePath : str):
        self.tokensPerFile[filePath] = self.initTokens(filePath=filePath)

    def initAllFilesTokens(self) -> None:
        for filePath in self.fileList:
            self.abriThread.add(function=self.directAdd, config=filePath, name=filePath)
        self.abriThread.run()


    def addFile(self, filePath : str) -> None:
        if not(os.path.exists(filePath)):
            raise FileNotFoundError('File not found :', filePath)
        self.tokensPerFile[filePath] = self.initTokens(filePath=filePath)


    def getTokens(self, filePath : str) -> TokenSequence:
        if filePath not in self.fileList:
            raise UnknownTokenError(f'fileName not add to tokenizer wait. Please add it before getting tokens :({filePath})')
        return self.tokensPerFile[filePath]

TokenizerObject = Tokenizer()
