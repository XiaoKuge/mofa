import json
from dora import Node, DoraStatus
import pyarrow as pa

from mae.kernel.utils.log import write_agent_log
from mae.kernel.utils.util import load_agent_config, load_dora_inputs_and_task
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
            agent_inputs = ['arxiv_research_task']
            if dora_event["id"] in agent_inputs:
                task_inputs, dora_result, task = load_dora_inputs_and_task(dora_event)
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='keyword_extractor.yml')
                inputs = load_agent_config(yaml_file_path)
                result = """ """
                if 'agents' not in inputs.keys():
                    inputs['task'] = task
                    result = run_dspy_agent(inputs=inputs)
                else:
                    result = run_crewai_agent(crewai_config=inputs)
                log_result = {"1, "+ inputs.get('log_step_name',"Step_one"):{task:result}}
                write_agent_log(log_type=inputs.get('log_type',None),log_file_path=inputs.get('log_path',None),data=log_result)
                result_dict = {'task':task,'keywords':result}
                print(result_dict)
                send_output("keyword_extractor_results", pa.array([json.dumps(result_dict)]),dora_event['metadata'])
                print('agent_output:', result)

                return DoraStatus.STOP

        return DoraStatus.CONTINUE