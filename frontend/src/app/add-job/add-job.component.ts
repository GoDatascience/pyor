import {Component, OnInit} from '@angular/core';
import {FormControl} from "@angular/forms";

import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';
import {ParamDefinition, Task} from "../add-task/task";


@Component({
  selector: 'app-add-job',
  templateUrl: './add-job.component.html',
  styleUrls: ['./add-job.component.css']
})
export class AddJobComponent implements OnInit {
  taskCtrl: FormControl;
  filtredTasks: any;
  tasks: Task[] = [];
  selectedTaskName: string;

  constructor() {
    this.taskCtrl = new FormControl();
    this.filtredTasks = this.taskCtrl.valueChanges
      .startWith(null)
      .map(task => this.filterTasks(task));
    this.mockTasks();
  }

  mockTasks() {
    let task: Task = new Task();
    task.name = "Train BitCoin";
    let param_definition_task = new ParamDefinition();
    param_definition_task.name = "Extension";
    param_definition_task.type = "text";
    let param_definition_2_task = new ParamDefinition();
    param_definition_2_task.name = "Size";
    param_definition_2_task.type = "number";
    task.param_definitions.push(param_definition_task);
    task.param_definitions.push(param_definition_2_task);
    this.tasks.push(task);

    let task2: Task = new Task();
    task2.name = "Train IBOVESPA";
    let param_definition_task2 = new ParamDefinition();
    param_definition_task2.name = "Extension";
    param_definition_task2.type = "text";
    let param_definition2_task2 = new ParamDefinition();
    param_definition2_task2.name = "Size";
    param_definition2_task2.type = "number";
    task2.param_definitions.push(param_definition_task2);
    task2.param_definitions.push(param_definition2_task2);
    this.tasks.push(task2);

    let task3: Task = new Task();
    task3.name = "Predict IBOVESPA";
    let param_definition_task3 = new ParamDefinition();
    param_definition_task3.name = "Date";
    param_definition_task3.type = "date";
    let param_definition2_task3 = new ParamDefinition();
    param_definition2_task3.name = "Rate";
    param_definition2_task3.type = "number";
    let param_definition3_task3 = new ParamDefinition();
    param_definition3_task3.name = "Use Cluster";
    param_definition3_task3.type = "boolean";
    task3.param_definitions.push(param_definition_task3);
    task3.param_definitions.push(param_definition2_task3);
    task3.param_definitions.push(param_definition3_task3);
    this.tasks.push(task3);

    let task4: Task = new Task();
    task4.name = "Predict BitCoin";
    let param_definition_task4 = new ParamDefinition();
    param_definition_task4.name = "Date";
    param_definition_task4.type = "date";
    let param_definition2_task4 = new ParamDefinition();
    param_definition2_task4.name = "Rate";
    param_definition2_task4.type = "number";
    let param_definition3_task4 = new ParamDefinition();
    param_definition3_task4.name = "Use Cluster";
    param_definition3_task4.type = "boolean";
    task4.param_definitions.push(param_definition_task4);
    task4.param_definitions.push(param_definition2_task4);
    task4.param_definitions.push(param_definition3_task4);
    this.tasks.push(task4);
  }

  filterTasks(taskName: string) {
    return taskName ? this.tasks.filter(task =>
    task.name.toLowerCase().indexOf(taskName.toLowerCase()) > 0 ||
    task.name.toLowerCase().indexOf(taskName.toLowerCase()) === 0) : this.tasks;
  }

  loadParams(taskName: string) {
    console.log("Load params for", this.getTask(taskName));
  }

  getSelectedTask(): Task {
    return this.getTask(this.selectedTaskName);
  }

  getTask(taskName: string) {
    return this.tasks.filter(task => task.name === taskName)[0];
  }

  startJob() {
    console.log(this.getSelectedTask());
    console.log("Run....");
  }

  ngOnInit() {
  }

}
