import React, { useEffect, useState} from 'react';
import axios from 'axios';
import {Link, useParams, useNavigate} from "react-router-dom";


const Voted = () => {
  const [candidate, setCandidate] = useState({});
  const [name, setName] = useState("");
  const [counter, setCounter] = useState(0);
  const {submitted, setSubmitted} = useState(false)
  
  const {id} = useParams();
  const navigate = useNavigate();

  const [errors,setErrors] = useState({})


  useEffect(() => {
    axios.get(`http://localhost:8000/api/candidate/${id}`)
    .then( (res) => {
      console.log(res.data);
      setName(res.data);
      setCounter(counter => counter + 1)
  })
  .catch( (err) => console.log(err) );
}, []);

  const onSubmitHandler = (e) => {
    if (submitted) {
      return;
    }
    e.preventDefault();
    axios.put(`http://localhost:8000/api/vote/${id}`,{
        name,
        counter
    })
    .then((res)=> {
      console.log(res.data)
      setSubmitted(true)
      navigate('/api/candidates')
    }).catch((err) => {
      console.log(err)
      setErrors(err.response.data.errors)
  })

}
       

  return (
    <div>
        <div> 
            <p>{candidate.name}</p> 
            <p>{candidate.pastTermStartDate}</p>
            <p>{candidate.pastTermEndDate}</p>
            <p>{candidate.party}</p>
            <p>{candidate.stance}</p>
            <p>{candidate.experience}</p>
            <form onSubmit={onSubmitHandler}>
              <input type="text" defaultValue={candidate.name} onChange={e => setName(e.target.value)}></input>
              <input type="checkbox"  defaultChecked={false} onClick={((e) => setCounter(e.target.value))}></input>
              <button>Vote for this Candidate</button>
            </form>
            <Link to={`/api/candidates`} className="btn border btn-info">Back to Candidates</Link>
        </div> 
    </div>
  )
}

export default Voted
