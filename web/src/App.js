import React, { useEffect, useState ,useRef} from 'react';
import axios from 'axios';
import {BASE_URL } from './api'

const App = () => {
  const ref = useRef()
  const [funds, setFunds] = useState([]);
  const [analysis, setAnalysis] = useState('');
  const [fund,setFund]= useState({});

  useEffect(() => {
    axios.get(`${BASE_URL}/scrape`)
      .then(response => {
        setFunds(response.data||[])
      })
      .catch(error => console.error(error));
  }, []);

  const handleAnalyze = () => {
    axios.post(`${BASE_URL}/analyze`, { prompt: 'Analyze mutual fund trends.' })
      .then(response => setAnalysis(response.data.analysis))
      .catch(error => console.error(error));
  };

  const handleSelectChange = () => {
    const code = ref.current.value;
    const fund = funds.find(fund=>fund.code === code)
    setFund(fund);
  }

  return (
    <div>
      <h1>Mutual Fund Dashboard</h1>
     <select onChange={handleSelectChange} ref={ref}>
      <option>Please select a fund</option>
      {funds.map((fund, index) =><option value={fund.code} key={fund.code}>{'('+fund.code+')' + fund.name}</option>)}
     </select>
    {fund.code? <div >
        <p>基金代码:{fund.code}</p>
        <p>基金名称:{fund.name}</p>
        <p>基金单位净值:{fund.nav}</p>
        <p>基金累计净值:{fund.anav}</p>
     </div>:null}
      <button onClick={handleAnalyze}>Analyze Trends</button>
      <p>{analysis}</p>
    </div>
  );
};

export default App;
