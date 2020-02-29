import React, { useState, useEffect } from 'react';
import Autocomplete, { createFilterOptions } from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';

import { User, UserID } from '../../models/models';
import { getSlackUsers } from '../../apiClient'

type IgnoreUsersInputProps = {
  value: UserID[];
  disabled: boolean;
  onChange: (userIds: UserID[]) => void;
}

export default function IgnoreUsersInput(props: IgnoreUsersInputProps) {

  const [userMap, setUserMap] = useState<Map<UserID, User>>(new Map());
  const [loading, setLoading] = useState(false);

  const getUserLabel = (opt: UserID) => {
    const user = userMap.get(opt);
    if (user == null) {
      return opt
    }

    return `@${user.name} | ${user.id}`
  }

  // Use user name to filter
  const filterOption = createFilterOptions({ stringify: getUserLabel })

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
        getOptionLabel={getUserLabel}
        filterOptions={filterOption}
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
