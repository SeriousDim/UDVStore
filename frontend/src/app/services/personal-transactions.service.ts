import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {IUser} from "../../interfaces/interfaces";
import {PeopleService} from "../login/services/people.service";
import {IOrder} from "../../interfaces/order";
import {environment} from "../../environments/environment";
import {ITransaction} from "../../interfaces/transaction";

@Injectable({
    providedIn: 'root'
})
export class PersonalTransactionsService {
    private _urlOrdersUser: string = environment.api_address + '/orders/';
    private _patchStatusOrders: string = environment.api_address + '/order/';

    constructor(
        private _http: HttpClient,
        private _peopleService: PeopleService,
    ) {
    }

    public getOrdersUser() {
        let user: any;
        this._peopleService.findUser.subscribe((res) => {
            user = res
        });
        const urlOrdersUser: string = this._urlOrdersUser + user!.id + '/';
        return this._http.get<ITransaction[]>(urlOrdersUser, this._peopleService.optionsForHttp);
    }

    public getAllOrders() {
        return this._http.get<ITransaction[]>(this._urlOrdersUser, this._peopleService.optionsForHttp);
    }

    public patchStatusOrders(id: number, statusNumber: number) {
        const patchStatusOrders: string = this._patchStatusOrders + id + '/';
        return this._http.patch(patchStatusOrders, {"status": statusNumber}, this._peopleService.optionsForHttp);
    }
}
