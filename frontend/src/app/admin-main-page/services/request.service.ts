import {ITransaction} from "../../../interfaces/transaction";
import {HttpClient} from "@angular/common/http";
import {PeopleService} from "../../login/services/people.service";
import {Injectable} from '@angular/core';
import {Observable} from "rxjs";
import {environment} from "../../../environments/environment";
import {ICoinsActivity} from "../../../interfaces/coinsActivity";

@Injectable({
    providedIn: 'root'
})
export class RequestService {
    private readonly _depositsUrl: string = environment.api_address + "/admin/deposits/"
    private readonly _approveUrl: string = environment.api_address + "/admin/approve/"
    private readonly _cancelUrl: string = environment.api_address + "/admin/cancel/";
    private readonly _getActivitiesUrl: string = environment.api_address + "/activities/"

    constructor(private _http: HttpClient, private _peopleService: PeopleService) {
    }

    public getRequests(): Observable<ITransaction[]> {
        return this._http.get<ITransaction[]>(this._depositsUrl, this._peopleService.optionsForHttp);
    }

    public approve(transaction: ITransaction, amount: number, description: string): Observable<Object> {
        return this._http.post(this._approveUrl, {
            'transaction_id': transaction.id,
            'amount': amount,
            'comment': description
        }, this._peopleService.optionsForHttp)
    }

    public cancel(transaction: ITransaction, description: string): Observable<Object> {
        return this._http.post(this._cancelUrl, {
            'transaction_id': transaction.id,
            'comment': description
        }, this._peopleService.optionsForHttp)
    }

    public getActivities(): Observable<ICoinsActivity[]> {
        return this._http.get<ICoinsActivity[]>(this._getActivitiesUrl, this._peopleService.optionsForHttp)
    }
}
