import { useEffect } from "react";

function Test() {
  useEffect(() => {
    async function fetchData() {
      const url = `${process.env.REACT_APP_BASE_URL}/tweets`;
      console.log(url);
      const response = await fetch(url);
      const data = await response.json();
      console.log(data);
    }
    fetchData();
  }, []);

  return <div>{`${process.env.REACT_APP_BASE_URL}`}</div>;
}

export default Test;
