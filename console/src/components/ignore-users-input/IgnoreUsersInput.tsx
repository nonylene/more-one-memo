import React, { useState, useEffect } from 'react';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';

import { User } from '../../models/models';
import { getSlackUsers } from '../../apiClient'

type IgnoreUsersInputProps = {
  value: User[];
  onChange: (users: User[]) => void;
}

const userToLabel = (user: User) => `@${user.name} | ${user.id}`

export default function IgnoreUsersInput(props: IgnoreUsersInputProps) {

  const [allUsers, setAllUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    getSlackUsers()
      .then(setAllUsers).then(() => setLoading(false))
      .catch(console.log);
  }, []);

  return (
    <div className="IgnoreUsersInput">
      <Autocomplete
        multiple
        options={allUsers}
        loading={loading}
        loadingText="Loading Slack users..."
        getOptionLabel={userToLabel}
        value={props.value}
        onChange={(_, values) => props.onChange(values)}
        renderInput={params => (
          <TextField
            {...params}
            label="Ignore users"
            placeholder="Users"
            fullWidth
          />
        )}
      />
    </div>
  );
}
