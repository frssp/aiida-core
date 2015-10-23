# -*- coding: utf-8 -*-

from aiida.orm import JobCalculation
from aiida.orm.data.parameter import ParameterData 
from aiida.common.utils import classproperty
from aiida.common.exceptions import InputValidationError
from aiida.common.exceptions import ValidationError
from aiida.common.datastructures import CalcInfo, CodeInfo
from aiida.orm.data.float import FloatData
import json

__copyright__ = u"Copyright (c), 2015, ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE " \
                u"(Theory and Simulation of Materials (THEOS) and National Centre " \
                u"for Computational Design and Discovery of Novel Materials (NCCR MARVEL)), " \
                u"Switzerland and ROBERT BOSCH LLC, USA. All rights reserved."
__license__ = "MIT license, see LICENSE.txt file"
__version__ = "0.4.1"

class FloatsumCalculation(JobCalculation):
    """
    A generic plugin for calculations based on the ASE calculators.
    
    Requirement: the node should be able to import ase
    """
    
    def _init_internal_params(self):
        super(FloatsumCalculation, self)._init_internal_params()
        
        self._INPUT_FILE_NAME = 'in.json'
        self._OUTPUT_FILE_NAME = 'out.json'
        self._default_parser = 'floatsum'
        
    @classproperty
    def _use_methods(cls):
        """
        Additional use_* methods for the namelists class.
        """
        retdict = JobCalculation._use_methods
        retdict.update({
            "floatdata1": {
               'valid_types': FloatData,
               'additional_parameter': None,
               'linkname': 'floatdata1',
               'docstring': ("Use a node that specifies the input float"),
               },
            "floatdata2": {
               'valid_types': FloatData,
               'additional_parameter': None,
               'linkname': 'floatdata2',
               'docstring': ("Use a node that specifies the input float"),
               },
            })
        return retdict
    
    def _prepare_for_submission(self,tempfolder, inputdict):        
        """
        This is the routine to be called when you want to create
        the input files and related stuff with a plugin.
        
        :param tempfolder: a aiida.common.folders.Folder subclass where
                           the plugin should put all its files.
        :param inputdict: a dictionary with the input nodes, as they would
                be returned by get_inputs_dict (with the Code!)
        """
        try:
            floatdata1 = inputdict.pop(self.get_linkname('floatdata1'))
        except KeyError:
            raise InputValidationError("Float data1 is not specified for this calculation")

        try:
            floatdata2 = inputdict.pop(self.get_linkname('floatdata2'))
        except KeyError:
            raise InputValidationError("Float data2 is not specified for this calculation")


        if (not isinstance(floatdata1, FloatData)) or (not isinstance(floatdata2, FloatData)):
            raise InputValidationError("Data is not of type FloatData.")

        try:
            code = inputdict.pop(self.get_linkname('code'))
        except KeyError:
            raise InputValidationError("No code specified for this calculation.")

        if inputdict:
            raise ValidationError("Cannot add other nodes beside floatdata1 and floatdata2.")

        ##############################
        # END OF INITIAL INPUT CHECK #
        ##############################
        
        # input_json = parameters.get_dict()
        input_json = {"x1": floatdata1.value, "x2": floatdata2.value}

        # write all the input to a file
        input_filename = tempfolder.get_abs_path(self._INPUT_FILE_NAME)
        with open(input_filename, 'w') as infile:
            json.dump(input_json, infile)
        
        # ============================ calcinfo ================================
        
        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.local_copy_list = []
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = [self._OUTPUT_FILE_NAME]
        
        codeinfo = CodeInfo()
        codeinfo.cmdline_params = [self._INPUT_FILE_NAME,self._OUTPUT_FILE_NAME]
        codeinfo.code_uuid = code.uuid
        calcinfo.codes_info = [codeinfo]
        
        return calcinfo

