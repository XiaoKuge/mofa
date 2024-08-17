import json
from dora import Node, DoraStatus
import pyarrow as pa

from mae.kernel.utils.log import write_agent_log
from mae.kernel.utils.util import load_agent_config
from mae.run.run import run_dspy_agent, run_crewai_agent
from mae.utils.files.dir import get_relative_path
from mae.utils.files.read import read_yaml



class Operator:
    inputs_data = []
    agents_inputs = ['web_search_task']
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['web_search_task']
            if dora_event["id"] in agent_inputs:
                task = dora_event["value"][0].as_py()
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='web_search_agent.yml')
                inputs = load_agent_config(yaml_file_path)
                if inputs.get('check_log_prompt', None) is True:
                    log_config = {}
                    agent_config =  read_yaml(yaml_file_path).get('AGENT', '')
                    agent_config['task'] = task
                    log_config['1 , Web_Search_Config'] = agent_config
                    write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
                                    data=log_config)
                if 'agents' not in inputs.keys():
                    inputs['task'] = task
                    result = run_dspy_agent(inputs=inputs)
                else:
                    result = run_crewai_agent(crewai_config=inputs)
                log_result = {'2, Web Search Resource ' :{d.get('name'):d.get('url') for d in json.loads(result.get('web_search_resource'))}}
                log_result['3, Web Search Answer '] = result.get('web_search_results')
                write_agent_log(log_type=inputs.get('log_type',None),log_file_path=inputs.get('log_path',None),data=log_result)
                result['task'] = task
                send_output("web_search_aggregate_output", pa.array([json.dumps(result)]),dora_event['metadata'])
                send_output("web_search_results", pa.array([json.dumps({'web_search_results':result.get('web_search_results')})]),dora_event['metadata'])
                send_output("web_search_resource", pa.array([json.dumps({'web_search_resource':result.get('web_search_resource')})]),dora_event['metadata'])
                print('agent_output:', result)
        return DoraStatus.CONTINUE