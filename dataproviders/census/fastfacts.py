import io
from typing import List
import pandas as pd
from dataproviders.providers import AsyncDataProvider


class AsyncFastFacts(AsyncDataProvider):
    countytypestr = 'county'
    citytypestr = 'city'
    url_format: str = 'https://www.census.gov/quickfacts/csv/{}{}{},US/PST045219'

    async def get_datadf(self, *, city: str=None, county: str=None, state=None, state_abbr: str=None) -> pd.DataFrame:
        self.errcheck(city, county, state, state_abbr)
        url = None
        if city:
            url = self.get_city_url(city, state_abbr)
        elif county:
            url = self.get_county_url(county, state_abbr)
        else:
            url = self.get_state_url(state_abbr)

        strdata = await self.get(url)
        dataio = io.StringIO(strdata)
        return pd.read_csv(dataio)

    def get_county_url(self, county: str, state_abbr: str):
        return self.url_format.format(
            county.replace(' ', ''),
            self.countytypestr,
            state_abbr)

    def get_city_url(self, city: str, state_abbr: str):
        return self.url_format.format(
            city.replace(' ', ''),
            self.citytypestr,
            state_abbr)

    def get_state_url(self, state_abbr: str):
        return self.url_format.format('', '', state_abbr)

    async def get_city_data(self, city: str, state_abbr: str) -> pd.DataFrame:
        data = await self.get(self.get_city_url(city, state_abbr))
        return pd.read_csv(data)

    async def get_county_data(self, county: str, state_abbr: str) -> pd.DataFrame:
        data = await self.get(self.get_county_url(county, state_abbr))
        return pd.read_csv(data)

    async def get_state_data(self, state_abbr: str, state_fullname: str) -> pd.DataFrame:
        data = await self.get(self.get_state_url(state_abbr))
        datafilelikeobj = io.StringIO(data.decode())
        df = pd.read_csv(datafilelikeobj)
        dfact = data['Fact']
        cdf = pd.DataFrame(pd.DataFrame(df[state_fullname]).transpose())
        cdf.columns = dfact
        return cdf

    def errcheck(self, city: str, county: str, state_fullname, state_abbr: str):
        errors: List[str] = []
        if city and county:
            errors.append('Must choose city or county, not both')
        if city and not state_abbr:
            errors.append('Must provide state_abbr of city')
        if county and not state_abbr:
            errors.append('Must provide state of county')
        if state_fullname and not state_abbr or state_abbr and not state_fullname:
            errors.append('Must provide states full name and abbreviation')

        if errors:
            numerrs = len(errors)
            if numerrs < 2:
                raise RuntimeError(errors[0])
            else:
                errmsgstart = f'{numerrs} errors:'
                numederrmsglist = [f'{i}. {err}' for i, err in enumerate(errors)]
                finalmsg = '\n'.join(errmsgstart + numederrmsglist)
                raise RuntimeError(finalmsg)
