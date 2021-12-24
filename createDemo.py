from utils.CommandLineArgs import CommandLineArgs
import sys
from utils.functions import arnold_cat_map


args = CommandLineArgs(sys.argv, 'file:str:!', 'original:str:!', 'identifier:str:DEMO')
identifier = args.get('identifier')
seq = arnold_cat_map(filename=args.get('original'), 
                    outname=f'images/final/{identifier}.png', 
                    retain_final=True, 
                    image_key=identifier, 
                    sequence_id=None, 
                    append_to_text_file=f'data/{identifier}.txt',
                    retain_steps=True)