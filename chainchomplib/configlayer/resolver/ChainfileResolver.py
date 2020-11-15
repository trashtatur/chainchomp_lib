import os
import yaml

from chainchomplib import LoggerInterface
from chainchomplib.configlayer.model.ChainfileModel import ChainfileModel

from chainchomplib.abstracts.AbstractResolver import AbstractResolver
from chainchomplib.configlayer.verify.SchemaVerifier import SchemaVerifier
from chainchomplib.configlayer.verify.schema.ChainfileSchema import ChainfileSchema
from chainchomplib.exceptions.Exceptions import NotValidException


class ChainfileResolver(AbstractResolver):

    @staticmethod
    def resolve_config_file(path_to_file: str):

        if not os.path.isfile(path_to_file):
            return

        with open(path_to_file) as chainfile:
            try:
                chainfile_data = yaml.safe_load(chainfile)
            except yaml.YAMLError:
                # TODO handle Exception
                LoggerInterface.error(f'The provided file is not in valid yaml syntax: {path_to_file}')
                return

        try:
            SchemaVerifier.verify(chainfile_data, ChainfileSchema())
        except NotValidException:
            return

        chainlink_sub_dict: dict = chainfile_data.get('chainlink')
        chainlink_name = chainlink_sub_dict.get('name')
        chainlink_next = chainlink_sub_dict.get('next')
        chainlink_previous = chainlink_sub_dict.get('previous')
        start = chainfile_data.get('start')
        stop = chainfile_data.get('stop')
        adapter_type = chainfile_data.get('adapter')
        profile = chainfile_data.get('profile')

        model = ChainfileModel(
            chainfile_data['project'],
            chainlink_name
        )

        if chainlink_next is not None:
            model.next_link = chainlink_next

        if chainlink_previous is not None:
            model.previous_link = chainlink_previous

        if start is not None:
            model.start = start

        if stop is not None:
            model.stop = stop

        if adapter_type is not None:
            model.adapter = adapter_type

        if profile is not None:
            model.profile = profile

        return model
