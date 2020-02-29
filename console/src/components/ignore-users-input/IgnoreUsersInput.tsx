import React, { useState, useEffect } from 'react';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';

import { User, UserID } from '../../models/models';
import { getSlackUsers } from '../../apiClient'

type IgnoreUsersInputProps = {
  value: UserID[];
  disabled: boolean;
  onChange: (userIds: UserID[]) => void;
}

const userToLabel = (user: User) => `@${user.name} | ${user.id}`

export default function IgnoreUsersInput(props: IgnoreUsersInputProps) {

  const [userMap, setUserMap] = useState<Map<UserID, User>>(new Map());
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    getSlackUsers()
      .then(users => {
        const map = new Map(users.map(c => [c.id, c]))
        setUserMap(map)
      })
      .then(() => setLoading(false))
      .catch(console.log);
  }, []);

  return (
    <div className="IgnoreUsersInput">
      <Autocomplete
        multiple
        options={Array.from(userMap.keys())}
        loading={loading}
        disabled={props.disabled}
        loadingText="Loading Slack users..."
        getOptionLabel={opt => userToLabel(userMap.get(opt)!)}
        value={props.value}
        onChange={(_, values) => props.onChange(values)}
        renderInput={params => (
          <TextField
            {...params}
            label="Ignore users"
            placeholder="User"
            fullWidth
          />
        )}
      />
    </div>
  );
}
