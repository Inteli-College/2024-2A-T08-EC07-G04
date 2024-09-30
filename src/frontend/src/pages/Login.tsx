import LoginForm from "../components/LoginForm"

export default function Login() {
    return (
        <div className="relative w-screen h-screen bg-[url('/bg.png')] bg-cover bg-center">
            
            <div className="absolute inset-0 bg-[#000475] bg-opacity-50"></div>
            <div className="relative z-10 flex justify-center items-center h-full">
                <LoginForm />
            </div>
        </div>
    )
}
