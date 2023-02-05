import React, { useState } from 'react'
import axios from 'axios';


import React, { useState } from 'react';
import axios from 'axios';
const UserForm = ()=> {
    const [name, setName] = useState("");
    const [pastTermStartDate, setPastTermStartDate] = useState("1/1/1900");
    const [pastTermEndDate, setPastTermEndDate] = useState("1/1/1900");
    const [party, setParty] = useState("");
    const [stance, setStance] = useState("");
    const [experience, setExperience] = useState("");

    //Create an array to store errors from the API
    const [errors, setErrors] = useState({}); 
    const onSubmitHandler = e => {
        e.preventDefault();
        //Send a post request to our API to create a Book
        axios.post('http://localhost:8000/api/contender', {
            name,
            pastTermStartDate,
            pastTermEndDate,
            party,
            experience,
            stance
        }
            .then(res=>console.log(res)) // If successful, do something with the response. 
            .catch(err=>{
                setErrors(err.response.data.errors)
                // const errorResponse = err.response.data.errors; // Get the errors from err.response.data
                // const errorArr = []; // Define a temp error array to push the messages in
                // for (const key of Object.keys(errorResponse)) { // Loop through all errors and get the messages
                //     errorArr.push(errorResponse[key].message)
                // }
                // Set Errors
                // setErrors(errorArr);
            })          
    )}
    return (
        <div>
            <form onSubmit={onSubmitHandler}>
                {errors.map((err, index) => <p key={index}>{err}</p>)}
                <p>
                    <label>Name:</label>
                    <input type="text" onChange={e => setName(e.target.value)} />
                    {errors.name && <span>{errors.Name.message}</span>}<br></br>
                </p>
                <p>
                    <label>Past Term Start Date</label>
                    <input type="date" onChange={e => setPastTermStartDate(e.target.value)} />
                    {errors.pastTermStartDate && <span>{errors.pastTermStartDate.message}</span>}<br></br>
                </p>
                <p>
                    <label>Past Term End Date</label>
                    <input type="date" onChange={e => setPastTermEndDate(e.target.value)} />
                    {errors.pastTermStartDate && <span>{errors.pastTermStartDate.message}</span>}<br></br>
                </p>
                <p>
                    <label>Party</label>
                    <input type="text" onChange={e => setParty(e.target.value)} />
                    {errors.party && <span>{errors.party.message}</span>}<br></br>
                </p>
                <p>
                    <label>Experience</label>
                    <input type="text" onChange={e => setExperience(e.target.value)} />
                    {errors.experience && <span>{errors.experience.message}</span>}<br></br>
                </p>
                <input type="submit" />
            </form>
        </div>
    )
}
export default UserForm;

