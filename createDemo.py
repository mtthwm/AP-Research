from utils.CommandLineArgs import CommandLineArgs
import sys
from utils.functions import arnold_cat_map


args = CommandLineArgs(sys.argv, 'file:str:!', 'original:str:!')
seq = arnold_cat_map(filename=args.get('original'), 
                    outname='images/final/DEMO.png', 
                    retain_final=True, 
                    image_key='DEMO', 
                    sequence_id=None, 
                    append_to_text_file='data/DEMO.txt',
                    retain_steps=True)