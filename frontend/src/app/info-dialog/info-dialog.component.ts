import { Component } from '@angular/core';
import {MdDialogRef} from "@angular/material";

@Component({
  selector: 'app-info-dialog',
  templateUrl: './info-dialog.component.html',
  styleUrls: ['./info-dialog.component.css']
})
export class InfoDialogComponent {
  message = "Info";

  constructor(public dialogRef: MdDialogRef<InfoDialogComponent>){}

  closeModal() {
    this.dialogRef.close(false);
  }
}
