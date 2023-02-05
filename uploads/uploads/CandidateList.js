import React, {useState, useEffect} from 'react'
import axios from 'axios'
import { Link} from 'react-router-dom';

const CandidateList = () => {   
    const [candidateList, setCandidateList] = useState([]);

    useEffect (() => {
        axios.get('http://localhost:8000/api/candidates', {withCredentials:true})
            .then((res) => {
                console.log(res)
                setCandidateList(res.data)
            }).catch(err => {
                console.log(err)
            })
    }, []);

    const deleteSelection = (index) => {
        setCandidateList((prevState) => {
          let items = [...prevState];
          console.log(items);
          items.splice(index, 1);
          return items;
        });
      };

  return (
    <div>
        { 
            candidateList.map(candidate => (
                <div className="h5 container d-flex p-2 mx-auto my-2 justify-content-between border-top">
                    <Link to={`/api/candidate/${candidate._id}`}>
                        <label>{candidate.firstName} {candidate.lastName} 
                            <input type="radio"/>
                        </label>
                    </Link>
                    <button id="Delete" onClick={deleteSelection}>
                        ✗
                    </button>
                </div>
            ))
        }
    </div>
  )
}

export default CandidateList;