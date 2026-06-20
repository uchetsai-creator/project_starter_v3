# Debug Instrumentation Rules

## Requirements
* Do not modify business logic.
* Do not add instrumentation to files that are not listed in the selected module-data-flow.
* Clearly mark all debug code with `// DEBUG:` comments.
* Print the key data being passed between layers.

## Debug Format

```ts
// DEBUG: <Flow Name> - <Step Name>
console.group("<Flow Name> - <Step Name>");
console.log("<Label>", value);
console.groupEnd();
debugger;
```

Backend code should use `console.group` and `console.log`. Add `debugger` only when explicitly requested.

## Instrumentation Format 
* Only add instrumentation for steps that exist in code.

### 1. Frontend Form Component

Add in the form submit handler.

Placement:
Immediately after `new FormData(event.currentTarget)` and before calling `onSubmit`.

Print:

* FormData contents using `Object.fromEntries(formData.entries())`

Example:

```ts
const formData = new FormData(event.currentTarget);

// DEBUG: <Flow Name> - Form Submit
console.group("<Flow Name> - Form Submit");
console.log("FormData", Object.fromEntries(formData.entries()));
console.groupEnd();
debugger;

onSubmit(formData);
```

### 2. Page Submit Handler

Add before calling mutation.

Placement:
Immediately before `createMutation.mutate(...)`, `updateMutation.mutate(...)`, or equivalent.

Print:

* Mutation payload

Example:

```ts
const payload = {
  ...
};

// DEBUG: <Flow Name> - Mutation Payload
console.group("<Flow Name> - Mutation Payload");
console.log("Payload", payload);
console.groupEnd();
debugger;

createMutation.mutate(payload);
```

### 3. React Query Hook

Add inside `mutationFn` or `queryFn`.

Placement:
As the first statement inside `mutationFn` or `queryFn`.

Print:

* Hook input
* Query filters, if applicable

Example:

```ts
mutationFn: async (input) => {
  // DEBUG: <Flow Name> - Hook Mutation
  console.group("<Flow Name> - Hook Mutation");
  console.log("Input", input);
  console.groupEnd();
  debugger;

  return createEntity(input);
}
```

### 4. Frontend API Function

Add before the HTTP request.

Placement:
Immediately before `fetch`, `api.get`, `api.post`, `api.patch`, or equivalent.

Print:

* Request URL
* Request method
* Request body
* Query params, if applicable

Example:

```ts
// DEBUG: <Flow Name> - API Request
console.group("<Flow Name> - API Request");
console.log("URL", url);
console.log("Method", "POST");
console.log("Body", body);
console.groupEnd();
debugger;

const response = await fetch(url, {
  method: "POST",
  body: JSON.stringify(body)
});
```

Add after the HTTP response is parsed.

Placement:
Immediately after response JSON is parsed and before returning.

Print:

* Response body

Example:

```ts
const result = await response.json();

// DEBUG: <Flow Name> - API Response
console.group("<Flow Name> - API Response");
console.log("Response", result);
console.groupEnd();
debugger;

return result;
```

### 5. Backend Router

Usually do not add logs here unless the flow needs route matching confirmation.

If needed, add before calling the controller.

Print:

* HTTP method
* Route path
* Route params

### 6. Controller Request

Add at the beginning of the controller method.

Placement:
First statement inside the controller function.

Print:

* `request.params`
* `request.query`
* `request.body`

Example:

```ts
export async function postEntity(request: Request, response: Response) {
  // DEBUG: <Flow Name> - Controller Request
  console.group("<Flow Name> - Controller Request");
  console.log("Params", request.params);
  console.log("Query", request.query);
  console.log("Request Body", request.body);
  console.groupEnd();

  ...
}
```

### 7. Controller Validation

Add immediately after schema validation.

Placement:
Immediately after `schema.parse(...)`.

Print:

* Validated params
* Validated query
* Validated body

Example:

```ts
const body = createEntityBodySchema.parse(request.body);

// DEBUG: <Flow Name> - Controller Validation
console.group("<Flow Name> - Controller Validation");
console.log("Validated Body", body);
console.groupEnd();
```

### 8. Service Input

Add at the beginning of the service method.

Placement:
First statement inside the service function.

Print:

* Service input
* Important IDs

Example:

```ts
export async function createEntity(input: CreateEntityInput) {
  // DEBUG: <Flow Name> - Service Input
  console.group("<Flow Name> - Service Input");
  console.log("Input", input);
  console.groupEnd();

  ...
}
```

### 9. Service Business Rule Decision

Add immediately after a business-rule check or decision.

Placement:
Immediately after duplicate check, availability check, validation decision, approval decision, or allocation decision.

Print:

* Rule input
* Rule result
* Decision outcome

Example:

```ts
const existing = await repository.findByCode(input.code);

// DEBUG: <Flow Name> - Duplicate Check
console.group("<Flow Name> - Duplicate Check");
console.log("Result", existing);
console.log("Decision", existing ? "Reject duplicate" : "Allow create");
console.groupEnd();
```

### 10. Repository Lookup

Add before the database lookup.

Placement:
Immediately before `prisma.*.findUnique`, `findFirst`, or `findMany`.

Print:

* Lookup parameters
* Prisma `where` or filter object

Example:

```ts
const where = { code };

// DEBUG: <Flow Name> - Repository Lookup
console.group("<Flow Name> - Repository Lookup");
console.log("Parameters", where);
console.groupEnd();

const result = await prisma.entity.findUnique({ where });
```

### 11. Repository Lookup Result

Add immediately after the database lookup returns.

Placement:
Immediately after `await prisma.*.findUnique`, `findFirst`, or `findMany`.

Print:

* Lookup result

Example:

```ts
const result = await prisma.entity.findUnique({ where });

// DEBUG: <Flow Name> - Repository Lookup Result
console.group("<Flow Name> - Repository Lookup Result");
console.log("Result", result);
console.groupEnd();

return result;
```

### 12. Repository Create / Update / Delete

Add immediately before database write.

Placement:
Immediately before `prisma.*.create`, `update`, `delete`, or transaction call.

Print:

* Prisma payload
* `where`
* `data`

Example:

```ts
const payload = {
  data
};

// DEBUG: <Flow Name> - Repository Write
console.group("<Flow Name> - Repository Write");
console.log("Prisma Payload", payload);
console.groupEnd();

return prisma.entity.create(payload);
```

### 13. Prisma Transaction

Add immediately before `$transaction`.

Placement:
Immediately before `prisma.$transaction(...)`.

Print:

* Transaction input
* Operations included

Example:

```ts
// DEBUG: <Flow Name> - Prisma Transaction
console.group("<Flow Name> - Prisma Transaction");
console.log("Operations", ["inventory.update", "transactionLog.create"]);
console.log("Input", input);
console.groupEnd();

return prisma.$transaction(async (tx) => {
  ...
});
```

### 14. Controller Response

Add immediately before sending the response.

Placement:
Immediately before `response.json(...)` or `response.status(...).json(...)`.

Print:

* Response DTO
* Status code

Example:

```ts
const dto = toEntityDto(result);

// DEBUG: <Flow Name> - Controller Response
console.group("<Flow Name> - Controller Response");
console.log("Status", 201);
console.log("Response DTO", dto);
console.groupEnd();

response.status(201).json(dto);
```

### 15. React Query Invalidation

Add after successful mutation and before invalidating queries.

Placement:
Inside `onSuccess`, immediately before `queryClient.invalidateQueries(...)`.

Print:

* Query key
* Mutation result, if available

Example:

```ts
onSuccess: (result) => {
  // DEBUG: <Flow Name> - React Query Invalidation
  console.group("<Flow Name> - React Query Invalidation");
  console.log("Result", result);
  console.log("Query Key", ["entities"]);
  console.groupEnd();
  debugger;

  queryClient.invalidateQueries({
    queryKey: ["entities"]
  });
}
```

### 16. UI Refresh

Add only when there is an explicit UI refresh action.

Placement:
Immediately before clearing form state, closing edit mode, resetting selection, or updating local state.

Print:

* State before update
* State after update if available

Example:

```ts
// DEBUG: <Flow Name> - UI Refresh
console.group("<Flow Name> - UI Refresh");
console.log("Clearing edit state", selectedEntity);
console.groupEnd();
debugger;

setSelectedEntity(null);
```

## Completion Report

After implementation, report:

* Flow instrumented
* Files modified
* Debug locations inserted
* Data printed at each location
* Expected execution order

Example:

```text
Flow instrumented:
Create Location

Files modified:
- LocationCreateForm.tsx
- LocationPage.tsx
- locationHooks.ts
- locationApi.ts
- locations.controller.ts
- locations.service.ts
- locations.repository.ts

Expected execution order:
Only include steps that exist in the implementation flow.
Form Submit
→ Mutation Payload
→ Hook Mutation
→ API Request
→ Controller Request
→ Controller Validation
→ Service Input
→ Repository Lookup
→ Repository Lookup Result
→ Duplicate Check
→ Repository Write
→ Controller Response
→ API Response
→ React Query Invalidation
→ UI Refresh
```
