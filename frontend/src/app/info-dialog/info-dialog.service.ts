import {Injectable} from "@angular/core";
import {MdDialog, MdDialogRef} from "@angular/material";
import {InfoDialogComponent} from "./info-dialog.component";

@Injectable()
export class InfoDialogService {
  constructor(public dialog: MdDialog) {
  }

  showDialog(mensagem: string): MdDialogRef<InfoDialogComponent> {
    const dialogRef = this.dialog.open(InfoDialogComponent);
    dialogRef.componentInstance.message = mensagem;
    return dialogRef;
  }
}
