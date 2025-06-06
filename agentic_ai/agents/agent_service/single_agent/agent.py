import os, json, asyncio, inspect, functools, logging, os
from typing import Any, Awaitable, Callable, Dict, List

from openai import AsyncOpenAI, AsyncAzureOpenAI
from agents.base_agent import BaseAgent

from fastmcp import Client                     # still using MCP server
MCP_ENDPOINT = os.getenv("MCP_SERVER_URI", "http://localhost:8000")
client = Client(MCP_ENDPOINT)

async def _to_native(content) -> Any:
    try:
        return content.as_json()
    except Exception:
        try:
            return json.loads(content.text)
        except Exception:
            return content.text

async def get_all_customers():
    """List all customers with basic info."""
    async with client:
        response = await client.call_tool("get_all_customers")
        # Use the direct text response as in teststream.py
        return response[0].text

async def get_customer_detail(customer_id: int) -> Dict[str, Any]:
    """Get a full customer profile including their subscriptions."""
    async with client:
        # Use the correct parameter format with "params" wrapper
        response = await client.call_tool("get_customer_detail", {"params": {"customer_id": customer_id}})
        return response[0].text

async def get_subscription_detail(subscription_id: int) -> Dict[str, Any]:
    """Detailed subscription view → invoices (with payments) + service incidents."""
    async with client:
        # Use the correct parameter format with "params" wrapper
        response = await client.call_tool("get_subscription_detail", {"params": {"subscription_id": subscription_id}})
        return response[0].text

async def get_promotions():
    """Get all promotions."""
    async with client:
        response = await client.call_tool("get_promotions")
        response = await _to_native(response[0])
        if response['status_code'] == 200:
            return response['data']
        else:
            raise Exception(f"Error fetching promotions: {response['text']}")

async def get_eligible_promotions(customer_id: int):
    """Check if a customer is eligible for a promotion."""
    async with client:
        # Use the correct parameter format with "params" wrapper
        response = await client.call_tool("get_eligible_promotions", {"params": {"customer_id": customer_id}})
        response = await _to_native(response[0])
        if response['status_code'] == 200:
            return response['data']
        else:
            raise Exception(f"Error fetching eligible promotions: {response['text']}")

async def search_knowledge_base(query: str):
    async with client:
        # Use the correct parameter format with "params" wrapper
        res = await client.call_tool("search_knowledge_base", {"params": {"query": query, "topk": 2}})
        response = await _to_native(res[0])
        if response['status_code'] == 200:
            return response['data']
        else:
            raise Exception(f"Error fetching knowledge base: {response['text']}")

async def get_security_logs(cust_id: int):
    async with client:
        # Use the correct parameter format with "params" wrapper
        res = await client.call_tool("get_security_logs", {"params": {"customer_id": cust_id}})
        response = await _to_native(res[0])
        if response['status_code'] == 200:
            return response['data']
        else:
            raise Exception(f"Error fetching security logs: {response['text']}")

async def get_customer_orders(cust_id: int):
    async with client:
        # Use the correct parameter format with "params" wrapper
        res = await client.call_tool("get_customer_orders", {"params": {"customer_id": cust_id}})
        response = await _to_native(res[0])
        if response['status_code'] == 200:
            return response['data']
        else:
            raise Exception(f"Error fetching customer orders: {response['text']}")

async def get_data_usage(sub_id: int):
    async with client:
        # Use the correct parameter format with "params" wrapper
        res = await client.call_tool("get_data_usage", {"params": {
            "subscription_id": sub_id,
            "start_date": "2023-01-01",
            "end_date": "2099-01-01",
            "aggregate": True,
        }})
        response = await _to_native(res[0])
        if response['status_code'] == 200:
            return response['data']
        else:
            raise Exception(f"Error fetching data usage: {response['text']}")

async def get_billing_summary(cust_id: int):
    async with client:
        # Use the correct parameter format with "params" wrapper
        response = await client.call_tool("get_billing_summary", {"params": {"customer_id": cust_id}})
        # Return the direct text response as in teststream.py
        return response[0].text

async def update_subscription(sub_id: int):
    async with client:
        # Use the correct parameter format with "params" wrapper
        res = await client.call_tool("update_subscription", {"params": {
            "subscription_id": sub_id,
            "update": {"status": "inactive"}
        }})
        response = await _to_native(res[0])
        if response['status_code'] == 200:
            return response['data']
        else:
            raise Exception(f"Error updating subscription: {response['text']}")

async def unlock_account(cust_id: int):
    async with client:
        # Use the correct parameter format with "params" wrapper
        res = await client.call_tool("unlock_account", {"params": {"customer_id": cust_id}})
        response = await _to_native(res[0])
        if response['status_code'] == 200:
            return response['data']
        else:
            raise Exception(f"Error unlocking account: {response['text']}")

TOOL_FUNCS: Dict[str, Callable[..., Awaitable[Any]]] = {
    fn.__name__: fn
    for fn in [
        get_all_customers,
        get_customer_detail,
        get_subscription_detail,
        get_promotions,
        get_eligible_promotions,
        search_knowledge_base,
        get_security_logs,
        get_customer_orders,
        get_data_usage,
        get_billing_summary,
        update_subscription,
        unlock_account,
    ]
}

# Build the JSON-schema list OpenAI needs.
#    We read each coroutine's signature so you don’t hand-write enums.
def _pytype_to_json(p):
    from typing import get_origin, get_args
    origin = get_origin(p) or p
    if origin is int:
        return "integer"
    if origin is float:
        return "number"
    if origin in (str, bytes):
        return "string"
    if origin is bool:
        return "boolean"
    if origin in (dict, Dict):
        return "object"
    if origin in (list, List):
        return "array"
    return "string"  # fallback

FUNCTION_SCHEMAS: List[dict] = []
for name, fn in TOOL_FUNCS.items():
    sig = inspect.signature(fn)
    properties, required = {}, []
    for param in sig.parameters.values():
        if param.kind is param.VAR_KEYWORD:
            continue
        jtype = _pytype_to_json(param.annotation)
        properties[param.name] = {"type": jtype}
        if param.default is param.empty:
            required.append(param.name)
    FUNCTION_SCHEMAS.append(
        {
            "name": name,
            "description": fn.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        }
    )
TOOLS = [{"type": "function", "function": spec} for spec in FUNCTION_SCHEMAS]

class Agent(BaseAgent):
    """
    Pure-OpenAI implementation that fulfils the BaseAgent contract.
    Persists chat history via the provided `state_store`.
    """

    def __init__(self, state_store: Dict[str, Any], session_id: str) -> None:
        super().__init__(state_store, session_id)

        # SDK auth – works for both “normal” and Azure-OpenAI endpoints
        if self.azure_openai_endpoint:
            # 🔧 use the ASYNC version
            self._client = AsyncAzureOpenAI(
                api_key=self.azure_openai_key,
                api_version=self.api_version or "2024-02-15-preview",
                azure_endpoint=self.azure_openai_endpoint,
            )
            self.model = self.azure_deployment
        else:
            self._client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = self.openai_model_name or "gpt-4o"
        # `messages` is the canonical chat transcript the SDK expects
        # Initialise it with any persisted history.
        self.messages: List[Dict[str, str]] = self.chat_history.copy()

    # ------------ INTERNAL helper to talk to the model ------------------- #
    async def _stream_completion(self, extra):
        return await self._client.chat.completions.create(
            model=self.model,
            messages=self.messages + extra,
            tools=TOOLS,
            stream=True,
        )

    # ------------ PUBLIC API required by BaseAgent ----------------------- #
    async def chat_async(self, prompt: str, tool_timeout: int = 90) -> str:
        """Send a prompt, auto-run any requested tool, return the assistant’s reply."""
        ######################################################################
        # 1)  Add user message to the transcript                             #
        ######################################################################
        self.messages.append({"role": "user", "content": prompt})

        ######################################################################
        # 2)  First completion – let the model decide if it needs a tool     #
        ######################################################################
        fn_name = None
        args = {}
        answer_chunks: List[str] = []

        # ---------- first stream: tool detection ---------------------------------
        async for chunk in await self._stream_completion([]):
            if not chunk.choices:          # ← guard against keep-alive / done
                continue

            choice = chunk.choices[0]
            delta  = choice.delta

            if delta.content:
                answer_chunks.append(delta.content)
                logging.debug(delta.content, end="", flush=True)

            # tool call?
            if delta.tool_calls:
                tool_call = delta.tool_calls[0]
                fn_name   = tool_call.function.name
                args      = json.loads(tool_call.function.arguments or "{}")
                break


        # If no tool call, we already streamed the whole answer
        if fn_name is None:
            assistant_reply = "".join(answer_chunks)
            self.messages.append({"role": "assistant", "content": assistant_reply})
            self._persist_state()
            return assistant_reply

        ######################################################################
        # 3)  Execute the Python coroutine corresponding to that tool        #
        ######################################################################
        tool_fn = TOOL_FUNCS.get(fn_name)
        if tool_fn is None:
            tool_result = {"error": f"Unknown tool: {fn_name}"}
        else:
            try:
                tool_result = await asyncio.wait_for(tool_fn(**args), timeout=tool_timeout)
            except Exception as exc:
                logging.exception("Tool execution failed")
                tool_result = {"error": str(exc)}

        ######################################################################
        # 4)  Second completion – give model the tool output                 #
        ######################################################################
        # First, record the call & result in the message log
        self.messages.extend(
            [
                {
                    "role": "assistant",
                    "content": None,
                    "function_call": {"name": fn_name, "arguments": json.dumps(args)},
                },
                {
                    "role": "function",
                    "name": fn_name,
                    "content": json.dumps(tool_result),
                },
            ]
        )

        # Now ask the model to finish the reply
        # ---------- second stream: final answer ----------------------------------
        full_answer_chunks: List[str] = []

        async for chunk in await self._stream_completion([]):
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            if delta.content:
                full_answer_chunks.append(delta.content)
                logging.debug(delta.content, end="", flush=True)


        assistant_reply = "".join(full_answer_chunks)
        self.messages.append({"role": "assistant", "content": assistant_reply})

        ######################################################################
        # 5)  Persist transcript + arbitrary state to the state_store        #
        ######################################################################
        self._persist_state()
        return assistant_reply

    # ------------ Small helper ------------------------------------------- #
    def _persist_state(self) -> None:
        """Dump chat transcript + any extra state into the store."""
        # save chat history
        self.state_store[f"{self.session_id}_chat_history"] = self.messages
        # example of saving arbitrary state:
        # self._setstate({"last_msg_id": len(self.messages)})