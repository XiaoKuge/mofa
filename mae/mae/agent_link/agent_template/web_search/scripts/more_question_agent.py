import json
from dora import Node, DoraStatus
import pyarrow as pa

from mae.kernel.utils.log import write_agent_log
from mae.kernel.utils.util import load_agent_config
from mae.run.run import run_dspy_agent, run_crewai_agent
from mae.utils.files.dir import get_relative_path
from mae.utils.files.read import read_yaml



class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['web_search_aggregate_output']
            if dora_event["id"] in agent_inputs:
                dora_result = json.loads(dora_event["value"][0].as_py())
                # yaml_file_path = 'use_case/more_question_agent.yml'
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='more_question_agent.yml')
                inputs = load_agent_config(yaml_file_path)
                log_result = {}
                if inputs.get('check_log_prompt', None) is True:
                    log_config = read_yaml(yaml_file_path).get('AGENT', '')
                    log_config['Task'] = dora_result.get('task')
                    log_result['3 , More Question Config'] = log_config
                write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
                                data=log_result)
                result = """
                                """
                if 'agents' not in inputs.keys():
                    inputs['context'] = dora_result.get('web_search_results')
                    inputs['input_fields'] = {'web_search_resource': json.dumps(dora_result.get('web_result')),'search_task':dora_result.get('task')}
                    result = run_dspy_agent(inputs=inputs)
                else:
                    result = run_crewai_agent(crewai_config=inputs)
                log_result = {"4, More Question Result":result}
                write_agent_log(log_type=inputs.get('log_type',None),log_file_path=inputs.get('log_path',None),data=log_result)
                # web_search_result = {'more_question_results':result,'task':dora_result.get('task'),'web_search_results':dora_result.get('web_search_results'),'web_search_resource':json.dumps(dora_result.get('web_search_resource'))}
                dora_result.update({'more_question_results':result})
                send_output("web_search_aggregate_output", pa.array([json.dumps(dora_result)]), dora_event['metadata'])
                send_output("more_question_results", pa.array([json.dumps({'more_question_results':result})]), dora_event['metadata'])
                print('agent_output:',{'more_question_results':result})
        return DoraStatus.CONTINUE