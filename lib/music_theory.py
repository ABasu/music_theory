#!/usr/bin/env python
# encoding=utf8

"""
Library for representing musical elements including notes and scales.
"""
import logging, sys

logging.basicConfig(format = '%(funcName)s %(asctime)-25s %(message)s', level = logging.DEBUG)

class Note(object):
    """
    Class for representing notes. Ech note is stored as a number, with middle C
    being 0. They may be accessed in other formats as well, including letters,
    solfege, Indian notation etc.
    """
    def __init__(self, note, tonic=None, fmt='western'):
        '''
        Representation of a note. Format can be 'western', 'western_solfege',
        'indian'

        Parameters
        ----------
        note : numeric or string
            This is parsed into a number.
        fmt : str, optional
            Notation format. The default is 'western'.

        Returns
        -------
        None.

        '''
        # Numeric to string representations
        int_str = {'western': {
            0: ['C', 'B#', 'Dbb'],
            1: ['C#', 'Db'],
            2: ['D', 'C##', 'Ebb'],
            3: ['D#', 'Eb'],
            4: ['E', 'Fb', 'D##'],
            5: ['F', 'E#'],
            6: ['F#', 'Gb'],
            7: ['G', 'F##', 'Abb'],
            8: ['G#', 'Ab'],
            9: ['A', 'G##', 'Bbb'],
            10:['A#', 'Bb'],
            11:['B', 'Cb', 'A##']}, 
        'indian': {
            0: 'S',
            1: 'Rb',
            2: 'R',
            3: 'Gb',
            4: 'G',
            5: 'M',
            6: 'M#',
            7: 'P',
            8: 'Db',
            9: 'D',
            10:'Nb',
            11:'N'}
        }

        if tonic is None:
            logging.error('Tonic required. Assuming C')
            tonic = 'C'
        
        if fmt == 'western':
            self.fmt = fmt
            self.int_str = int_str[fmt]
            self.str_int = {k:n for n in self.int_str for k in self.int_str[n]}
            self.tonic = self.set(tonic, fmt=fmt)
            self.note = self.set(note, fmt=fmt)
        elif fmt == 'western_solfege':
            logging.error('Solfege has not yet been implemented.')
            pass
        elif fmt == 'indian':
            # Get the western tonic and set it as Sa
            self.tonic = Note(tonic, fmt='western').get('numeric')
            
            self.fmt = fmt
            # Move note names up by the tonic offset, so the tonic becomes S
            self.int_str = {(i+self.tonic):n for i, n in int_str[fmt].items()}
            self.str_int = {k:n for n in self.int_str for k in self.int_str[n]}
            self.note = self.set(note, fmt=fmt)

    def get(self, fmt=None, note_fmt=None):
        '''
        Get the note in the specified format.

        Parameters
        ----------
        fmt : None or str, optional
            The system the notes. If None, then the self.format variable is used. 
            The default is 'numeric'.
        note_fmt: str or None
            The format a note needs to be in. e.g. Western notes can have multiple
            letter based representations. C is B# is Dbb. So, for the note of C
            having note_fmt=D will return Dbb.

        Returns
        -------
        note : numeric or str
            The note in the requested representation.
        '''
        if fmt is None:
            fmt = self.fmt
        if fmt == 'numeric':
            note = self.note
        else:
            note = self.num2note(fmt=fmt, note_fmt=note_fmt) 
        return note
    
    def set(self, note, fmt='western'):
        '''
        Set a note by converting to integer from string. Numeric notes are saved 
        directly as int.

        Parameters
        ----------
        note : numeric, str
            DESCRIPTION.
        fmt : TYPE, optional
            DESCRIPTION. The default is 'western'.

        Returns
        -------
        None.

        '''
        # If numeric, store note, otherwise convert to numeric
        if isinstance(note, (int, float)):
            self.note = int(note)
        else:
            self.note = self.note2num(note, fmt=fmt)
        return(self.note)

    def note2num(self, note, fmt=None):
        '''
        Parses the string representation of a note and returns the int representation.

        Parameters
        ----------
        note : str
            The note.
        fmt : str, optional
            Format. The default is None.

        Returns
        -------
        int

        '''
        if note is not None:
            octave = note.count('.')*-1 + note.count("'")*1
            note = note.strip(".'")
            note_num = self.str_int[note] + octave*12
        else:
            note_num = None
        
        return(note_num)

    def num2note(self, fmt=None, note_fmt=None):
        '''
        Takes a number and return the note representation

        Parameters
        ----------
        n : int
            Note number.
        fmt : TYPE, optional
            DESCRIPTION. The default is None.
        note_fmt : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        '''
        if fmt is None:
            fmt = self.fmt

        octave = int((self.note - self.tonic) / 12) if self.note >= self.tonic else int((self.note - self.tonic) / 12) - 1
        note_name = self.int_str[self.note % 12]
        
        # For western notes, we return the preferred note form
        if fmt == 'western':
            if note_fmt is None:
                note_name = note_name[0]
            else:
                note_idx = None
                for idx, nn in enumerate(note_name):
                    if note_fmt.upper() == nn[0]:
                        note_idx = idx
                        break
                if note_idx is None:
                    logging.error(f"Letter base '{note_fmt}' not in note {','.join(note_name)}. Returning default form {note_name[0]}")
                    note_idx = 0
                note_name = note_name[note_idx]
                
            if octave < 0:
                note_name = note_name + (-1*octave)*'.'
            else:
                note_name = note_name + octave * "'"
            
        return(note_name)