import {Component, OnInit, ViewChild} from '@angular/core';
import {FormControl} from "@angular/forms";

import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';
import {Param, Task} from "../add-task/task";
import {MdDatepicker} from "@angular/material";


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

  @ViewChild(MdDatepicker) picker: MdDatepicker<Date>;

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
    let param_definition_task = new Param("Extension", "text");
    let param_definition_2_task = new Param("Size", "number");
    task.params.push(param_definition_task);
    task.params.push(param_definition_2_task);
    this.tasks.push(task);

    let task2: Task = new Task();
    task2.name = "Train IBOVESPA";
    let param_definition_task2 = new Param("Extension", "text");
    let param_definition2_task2 = new Param("Size", "number");
    task2.params.push(param_definition_task2);
    task2.params.push(param_definition2_task2);
    this.tasks.push(task2);

    let task3: Task = new Task();
    task3.name = "Predict IBOVESPA";
    let param_definition_task3 = new Param("Date", "date");
    let param_definition2_task3 = new Param("Rate", "number");
    let param_definition3_task3 = new Param("Use Cluster", "boolean");
    task3.params.push(param_definition_task3);
    task3.params.push(param_definition2_task3);
    task3.params.push(param_definition3_task3);
    this.tasks.push(task3);

    let task4: Task = new Task();
    task4.name = "Predict BitCoin";
    let param_definition_task4 = new Param("Date", "date");
    let param_definition2_task4 = new Param("Rate", "number");
    let param_definition3_task4 = new Param("Use Cluster", "boolean");
    task4.params.push(param_definition_task4);
    task4.params.push(param_definition2_task4);
    task4.params.push(param_definition3_task4);
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
