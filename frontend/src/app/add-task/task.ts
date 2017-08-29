export class Task {
  name: string;
  script_file: File;
  auxiliar_files: File[] = [];
  param_definitions: ParamDefinition[] = [];
}

export class ParamDefinition {
  name: string;
  type: string;
}
