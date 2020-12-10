import click
import six
from PyInquirer import Token, prompt, style_from_dict, Separator
from pyfiglet import figlet_format

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None
    

# define command-line colorset
style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})

# log function : font/color/figuring(figlet module) available
def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))  # original log
        else:
            six.print_(colored(figlet_format(   # figlet log
                string, font=font), color))
    else:
        six.print_(string)  # non-color log
        
        
def getAnswerStatus(answer, answername, state):
    return answer.get(answername) == state


def confirmQ(when, message="", name=""):
    return {
        'type': 'confirm',
        'name': name,
        'message': message,
        'when': when
    }

def listQ(message="", name="", choicelist=[], exitloop=False):
    Q = [{
        'type': 'list',
        'name': name,
        'message': message,
        'choices': choicelist
    }]
    
    
    if exitloop:
        Q[0]['choices'].append(Separator("\n * * * * * * * * * * * * * * * * * * * * * \n"))
        Q[0]['choices'].append('exit')
        Q.append(
            confirmQ (
                message='do you want exit?',
                name= 'exit_confirm',
                when= lambda answers: getAnswerStatus(answers, 'excel', 'exit')
            )
        )
    return Q


