export const isAuthenticated = () => {
    const cookies = document.cookie.split(';').reduce((acc,cookie) => {
        const [key,value] = cookie.trim().split("=");
        acc[key] = value;
        return acc;
    }, {});

    console.log(cookies);

    return !!cookies["user_token"];
}