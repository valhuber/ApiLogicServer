const authProvider = {
    login: ({ username, password }) =>  {
        console.log( 'User name ', username, ' Password ', password);
        if ( username === 'admin' && password === 'p' ) {
            localStorage.setItem('username', username);
            return Promise.resolve();  
        }else {
            return Promise.reject();
        }
    // ...
},
logout: () => {
    localStorage.removeItem('username');
    return Promise.resolve();
},
checkError: ({error}) => {
    return Promise.resolve();

},
checkAuth: () => {
    return localStorage.getItem('username')
        ? Promise.resolve()
        : Promise.reject();
},
getPermissions: () => Promise.resolve(),

}

export default authProvider;