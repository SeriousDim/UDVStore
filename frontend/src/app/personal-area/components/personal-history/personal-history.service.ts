import {Injectable} from "@angular/core";
import {environment} from "../../../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {PeopleService} from "../../../login/services/people.service";
import {Observable} from "rxjs";
import {ITransaction} from "../../../../interfaces/transaction";


@Injectable({
    providedIn: 'root'
})
export class PersonalHistoryService
{
    private readonly _url: string = environment.api_address + "/profile/history/";
    private readonly _urlPerson: string = environment.api_address + "/admin/";

    constructor(private _http: HttpClient, private _peopleService: PeopleService) {}

    public getHistory(): Observable<ITransaction[]>
    {
        return this._http.get<ITransaction[]>(this._url, this._peopleService.optionsForHttp);
    }

    public getHistoryAdmin(idPerson: number): Observable<ITransaction[]> {
        return this._http.get<ITransaction[]>(this._urlPerson + idPerson + '/history/', this._peopleService.optionsForHttp);
    }
}
