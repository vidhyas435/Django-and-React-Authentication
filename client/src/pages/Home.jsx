import React, { useEffect } from "react";
import useAuth from "../hooks/useAuth";
import useUser from "../hooks/useUser";

export default function Home() {
  const { user } = useAuth();
  const getUser = useUser();

  useEffect(() => {
    getUser();
  }, []);

  return (
    <div className="container mt-3">
      <h2>
        <div className="row">
          <div className="mb-12">
            {user?.email !== undefined
              ? "List user Ethereum balance"
              : "Please login first"}
          </div>
        </div>
        <div className="py-5">
          {user?.balance?.map((res) => (
            <div key={res.account} className="d-flex flex-column">
              <p className="h4">Address: {res.account}</p>
              <p className="h4">Balance: {res.balance}</p>
            </div>
          ))}
        </div>
      </h2>
    </div>
  );
}
