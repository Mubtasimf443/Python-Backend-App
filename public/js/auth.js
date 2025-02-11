// بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ  ﷺ
// InshaAllah, By his marcy I will Gain Success


const signUpForm =document.getElementById('signup-page');
const LoginForm = document.getElementById('login-page');
let optForm=document.getElementById('otp-page');
function showOTPPage() {
    document.querySelectorAll('.auth-box').forEach(el => el.classList.add('hidden'));
    document.getElementById('otp-page').classList.remove('hidden')
}
function showLoginPage() {
    document.querySelectorAll('.auth-box').forEach(el => el.classList.add('hidden'));
    LoginForm.classList.remove('hidden')
}

function showSignUpPage() {
    document.querySelectorAll('.auth-box').forEach(el => el.classList.add('hidden'));
    signUpForm.classList.remove('hidden')
}
LoginForm.onsubmit =async function Login(event=new Event('submit')) {
    try {
        event.preventDefault()
        event.target.style.opacity=.65;
        let email = LoginForm.querySelector('#l-email').value.trim();
        let password = LoginForm.querySelector('#l-password').value.trim();
        let response= await fetch(window.location.origin +'/api/auth/login',{
            method :'post',
            body:JSON.stringify( { email, password }),
            headers :{'Content-Type':"application/json"}
        })
        if (response.status===200){
            window.location.assign('/')
            return;
        } else {
            let data = await response.json();
            if (data?.error?.message) return alert(data.error.message);
        }
    } catch (error) {
        console.log('Login Error');
        console.log(error);
    } finally {
        event.target.style.opacity=1;
    }
}


signUpForm.onsubmit =async function Signup(event=new Event('submit')) {
    try {
        event.preventDefault()
        event.target.style.opacity=.65;
        let name = signUpForm.querySelector('#s-name').value.trim();
        let email = signUpForm.querySelector('#s-email').value.trim();
        let password = signUpForm.querySelector('#s-password').value.trim();
        let response = await fetch(window.location.origin +'/api/auth/sign-up',{
            method :'post',
            body:JSON.stringify( { name, email, password }),
            headers :{'Content-Type':"application/json"}
        });
        (response.status === 201) && showOTPPage();

        let data=await response.json();
        console.log({data});
        (data?.error?.message !== undefined) && alert(data?.error?.message);
    } catch (error) {
        console.log('Signup Error');
        console.log(error);
    } finally {
        event.target.style.opacity=1;

    }
}

optForm.addEventListener('submit',async function OtpVerification(event =new Event('submit')) {
    try {
        event.preventDefault()
        let otp = document.getElementById('otp').valueAsNumber;
        let q= new URLSearchParams({pin:otp}).toString();
        let response=(await fetch(window.location.origin + '/api/auth/opt-verification?' + q));
        if (response.status===200) {
            window.location.assign('/')
        } else {
            let data=await response.json();
            if (data?.error?.message) return alert(data.error.message)
        }
    } catch (error) {
        console.log('OtpVerification Error');
        console.log(error);
    }
} )




let pathname =window.location.pathname;
document.querySelectorAll('.auth-box').forEach(el => el.classList.add('hidden'));
if (pathname.includes('login')) LoginForm.classList.remove('hidden');
if (pathname.includes('sign-in')) LoginForm.classList.remove('hidden');
if (pathname.includes('sign-up')) signUpForm.classList.remove('hidden');
if (pathname.includes('create-account')) signUpForm.classList.remove('hidden');
if (pathname.includes('register-account')) signUpForm.classList.remove('hidden');
if (pathname.includes('register')) signUpForm.classList.remove('hidden');