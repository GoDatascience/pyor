export class Task {
  name: string;
  script_file: File;
  auxiliar_files: File[] = [];
  param_definitions: Param[] = [];
}

export class Param {
  value: any;
  constructor(public name: string, public type: string) {}
}
